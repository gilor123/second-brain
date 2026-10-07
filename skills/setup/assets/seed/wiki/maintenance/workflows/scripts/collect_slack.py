#!/usr/bin/env python3
"""Build and check a Slack capture manifest from discovery pages.

manifest WORK_DIR SOURCES_JSON: validate all configured discovery searches, write
manifest.tsv, batch-N.tsv and warnings.txt. Exit 1 on coverage gaps, 2 on invalid
input. check WORK_DIR DAY_FILE: require exactly one block per Capture-ID with
required metadata. This structural check does not prove full message capture.

Discovery page p-S1-1.tsv (or S2/S3/B01...):
#<TAB>count<TAB>has_next(yes/no/denied)<TAB>cursor_used(- for page 1)
channel_id<TAB>kind(dm/gdm/channel)<TAB>label<TAB>message_ts<TAB>thread_ts(or -)<TAB>author_id
"""
import argparse
import json
import re
from pathlib import Path

STAMP = re.compile(r"\d+\.\d+")


def selection(config):
    if config.get('schema_version') != 1:
        raise ValueError('Unsupported sources schema_version')
    cfg = config['sources']['slack']
    for flag in ('include_sent', 'include_mentions', 'include_name_mentions', 'include_participated_dms'):
        if type(cfg.get(flag, False)) is not bool:
            raise ValueError(f'{flag} must be a JSON boolean, not text')
    if not cfg.get('user_id'):
        raise ValueError('Slack user_id must be resolved')
    channels = cfg.get('full_capture_channels', [])
    ids = [c['id'] for c in channels]
    if len(set(ids)) != len(ids) or any(not x for x in ids):
        raise ValueError('Full-capture channels must have unique nonempty IDs')
    expected = {}
    if cfg.get('include_sent') or cfg.get('include_participated_dms'):
        expected['S1'] = None
    if cfg.get('include_mentions'):
        expected['S2'] = None
    if cfg.get('include_name_mentions'):
        if not cfg.get('display_name'):
            raise ValueError('Name-mention discovery needs display_name')
        expected['S3'] = None
    excluded = set(cfg.get('excluded_channel_ids', []))
    for n, cid in enumerate(ids, 1):
        if cid in excluded:
            raise ValueError('A full-capture channel is also explicitly excluded')
        expected[f'B{n:02d}'] = cid
    if not expected:
        raise ValueError('No discovery scope selected')
    return cfg, expected


def parse_pages(work, expected):
    pages = {}
    for path in sorted(work.glob('p-*.tsv')):
        m = re.fullmatch(r'p-(S[123]|B\d+)-(\d+)\.tsv', path.name)
        if not m or m[1] not in expected or int(m[2]) < 1:
            raise ValueError(f'Unexpected discovery page {path.name}')
        lines = path.read_text(encoding='utf-8').splitlines()
        head = lines[0].split('\t') if lines else []
        if len(head) != 4 or head[0] != '#' or not head[1].isdigit() or head[2] not in ('yes', 'no', 'denied'):
            raise ValueError(f'Invalid page header: {path.name}')
        rows = []
        for line in lines[1:]:
            if not line:
                continue
            fields = line.split('\t')
            if len(fields) != 6:
                raise ValueError(f'Invalid row width: {path.name}')
            cid, kind, label, mts, root, author = fields
            if not cid or not author or kind not in ('dm', 'gdm', 'channel') or not STAMP.fullmatch(mts) or (root != '-' and not STAMP.fullmatch(root)):
                raise ValueError(f'Invalid discovery row: {path.name}')
            if expected[m[1]] is not None and cid != expected[m[1]]:
                raise ValueError(f'Channel mismatch: {path.name}')
            rows.append(fields)
        if len(rows) != int(head[1]):
            raise ValueError(f'Page count differs from recorded rows: {path.name}')
        sid, num = m[1], int(m[2])
        if num in pages.setdefault(sid, {}):
            raise ValueError(f'Duplicate page number: {path.name}')
        pages[sid][num] = (head[2], head[3], rows)
    return pages


def manifest(work, config_path):
    cfg, expected = selection(json.loads(config_path.read_text(encoding='utf-8')))
    pages = parse_pages(work, expected)
    warnings, hits = [], []
    for sid in expected:
        seq = pages.get(sid, {})
        if not seq:
            warnings.append(f'{sid}: required search did not run')
            continue
        nums = sorted(seq)
        if nums != list(range(1, nums[-1] + 1)):
            warnings.append(f'{sid}: missing discovery page')
        cursors = set()
        for n in nums:
            next_state, cursor, rows = seq[n]
            if n == 1 and cursor != '-':
                warnings.append(f'{sid}: first page cursor is not initial')
            if n > 1 and (cursor in ('', '-') or cursor in cursors):
                warnings.append(f'{sid}: absent or repeated pagination cursor')
            cursors.add(cursor)
            required_state = 'no' if n == nums[-1] else 'yes'
            if next_state != required_state:
                warnings.append(f'{sid} page {n}: pagination incomplete, denied, or inconsistent')
            for row in rows:
                hits.append((sid, row))
    work.joinpath('warnings.txt').write_text('\n'.join(warnings) + ('\n' if warnings else ''), encoding='utf-8')
    # Do not leave an apparently usable manifest from an earlier failed retry.
    for old in [work/'manifest.tsv', *work.glob('batch-*.tsv')]:
        if old.is_file():
            old.unlink()  # Generated scratch only, never captured source files.
    if warnings:
        print('\n'.join(warnings))
        return 1
    excludes = set(cfg.get('excluded_channel_ids', []))
    patterns = [re.compile(p, re.I) for p in cfg.get('excluded_label_patterns', [])]
    candidates = {}
    for sid, row in hits:
        cid, kind, label, mts, root, author = row
        if cid in excludes or any(p.search(label) for p in patterns):
            continue
        if sid == 'S1' and author != cfg['user_id']:
            raise ValueError('S1 result is not authored by the configured user')
        if kind in ('dm', 'gdm'):
            if not cfg.get('include_participated_dms') or sid != 'S1':
                continue
            key = (cid, '-')
        else:
            if sid == 'S1' and not cfg.get('include_sent'):
                continue
            key = (cid, root if root != '-' else mts)
        item = candidates.setdefault(key, {'kind':kind, 'cid':cid, 'label':label, 'roots':set(), 'sources':set()})
        if kind == 'channel':
            item['roots'].add(key[1])
        elif root != '-':
            item['roots'].add(root)
        item['sources'].add(sid)
    lines = []
    for i, item in enumerate(sorted(candidates.values(), key=lambda c:(c['kind'],c['cid'],sorted(c['roots']))), 1):
        lines.append('\t'.join([str(i), item['kind'], item['cid'], item['label'], ','.join(sorted(item['roots'])) or '-', ','.join(sorted(item['sources']))]))
    work.joinpath('manifest.tsv').write_text('#id\tkind\tchannel_id\tlabel\troots\tsources\n' + '\n'.join(lines) + ('\n' if lines else ''), encoding='utf-8')
    for n, start in enumerate(range(0, len(lines), 15), 1):
        work.joinpath(f'batch-{n}.tsv').write_text('\n'.join(lines[start:start+15])+'\n', encoding='utf-8')
    print(f'MANIFEST PASS searches={len(expected)} candidates={len(lines)}')
    return 0


def check(work, day_file):
    warning_file = work/'warnings.txt'
    if not warning_file.exists() or warning_file.read_text(encoding='utf-8').strip():
        raise ValueError('Discovery is not verified complete')
    lines = (work/'manifest.tsv').read_text(encoding='utf-8').splitlines()[1:]
    expected = {}
    for line in lines:
        if not line:
            continue
        fields = line.split('\t')
        if len(fields) != 6 or fields[0] in expected:
            raise ValueError('Malformed manifest')
        expected[fields[0]] = fields
    text = day_file.read_text(encoding='utf-8')
    parts = re.split(r'(?m)^## ', text)
    blocks = parts[1:]
    seen, errors = set(), []
    statuses = re.findall(r'(?m)^capture_status:[ \t]*([^\r\n]*)$', parts[0])
    if statuses != ['complete']:
        errors.append('Header must declare exactly one capture_status: complete')
    for block in blocks:
        ids = re.findall(r'(?m)^Capture-ID:[ \t]*(\d+)[ \t]*$', block)
        if len(ids) != 1 or ids[0] not in expected or ids[0] in seen:
            errors.append('Missing, unknown or duplicate Capture-ID')
            continue
        ident = ids[0]
        seen.add(ident)
        metadata = {}
        for field in ('Participants', 'Thread', 'Attachments'):
            values = re.findall(rf'(?m)^{field}:[ \t]*([^\r\n]*)$', block)
            if len(values) != 1 or not values[0].strip():
                errors.append(f'{ident}: missing, blank or duplicate {field}')
            else:
                metadata[field] = values[0].strip()
        # ID coverage alone must not allow an unrelated thread to stand in.
        row = expected[ident]
        thread = metadata.get('Thread', '')
        if not re.search(rf'(?<![A-Za-z0-9]){re.escape(row[2])}(?![A-Za-z0-9])', thread):
            errors.append(f'{ident}: missing source channel ID')
        for root in row[4].split(','):
            # Permalinks contain /p<timestamp-without-dot>; source IDs may be literal.
            exact = re.search(rf'(?<![\d.]){re.escape(root)}(?![\d.])', thread)
            permalink = re.search(rf'/p{re.escape(root.replace(".", ""))}(?!\d)', thread)
            if root != '-' and not exact and not permalink:
                errors.append(f'{ident}: missing source thread root {root}')
    for ident in sorted(set(expected)-seen):
        errors.append(f'{ident}: missing candidate block')
    if errors:
        print('CHECK FAIL\n'+'\n'.join(errors))
        return 1
    print(f'CHECK PASS candidates={len(expected)} blocks={len(blocks)}; full-text capture requires tool evidence')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['manifest', 'check'])
    parser.add_argument('work', type=Path)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    if not args.work.is_dir():
        parser.error('work directory must already exist')
    try:
        return manifest(args.work, args.input) if args.mode == 'manifest' else check(args.work, args.input)
    except (ValueError, KeyError, TypeError, OSError, re.error) as error:
        if args.mode == 'manifest':
            # Clear stale outputs even when malformed input failed before coverage validation.
            for old in [args.work/'manifest.tsv', *args.work.glob('batch-*.tsv')]:
                if old.is_file():
                    old.unlink()
            (args.work/'warnings.txt').write_text(str(error)+'\n', encoding='utf-8')
        print(f'INVALID: {error}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
