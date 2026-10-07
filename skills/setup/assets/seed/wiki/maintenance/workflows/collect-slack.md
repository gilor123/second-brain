# collect-slack

Capture selected Slack activity with deterministic discovery coverage and one complete file per day.

## Read first

Read `.claude/CLAUDE.md`, `wiki/.claude/CLAUDE.md`, `wiki/meta/INDEX.md`, and `wiki/meta/sources.json`. Collectors also read `raw/.claude/CLAUDE.md`. All paths are brain-root-relative. Use configured timezone and actual tested tool bindings, never guessed tool names.

## Zone rule

Write only `raw/inbox/slack/`, its lookup/run records, and this collector's scratch. Never synthesize or change curated sources.

Citation-path repairs during version publication or archival are the narrow wiki-write exception defined in the engine charter; require the engine lock and never change claim meaning or ingest-state.

## Procedure

During user-requested setup, run the connection checks using the onboarding defaults without another scope questionnaire. Sources remain inactive until checked; recurring runs require enabled state and `passed` or `passed_empty` evidence. An incomplete test is remaining work to finish, not a reason to abandon setup. `passed_empty` means access and complete empty discovery were verified; it never asserts a full-body read. Capture boundaries apply to dated streams; all-accessible sessions with no timestamps use stable IDs/version progress instead. Preserve explicit user overrides on resume.


1. Require enabled and verified (`passed` or `passed_empty`) `sources.slack`, Python 3 and actual search/full-thread/history/pagination capabilities. Acquire the Slack source lock. Use the user's timezone and previous completed day D; validate every timestamp against exact day boundaries. For initial tests, set a bounded test scope and never present it as a complete day.
2. Resolve user/channel IDs through tested tools; cache in `raw/inbox/slack/directory.md`. Respect configured exclusions. Run only selected discovery searches: S1 own sent messages, S2 direct mentions, S3 display-name mentions, and B01... for each configured full-capture channel. Participated DMs require S1 even if channel sent-message capture is off. Use native query syntax validated during setup, never assumed from this document. Include read and unread activity.
3. In a fresh work directory `maintenance/temp/slack-<day>-<run-id>/`, write every discovery page immediately as `p-<search-id>-<page>.tsv`. Header is `#<TAB>count<TAB>has_next<TAB>cursor_used`; count is THIS page's actual row count, has_next is yes/no/denied, cursor is the actual cursor or `-` on page one. Body has six tab-separated fields: channel_id, kind (dm/gdm/channel), label, message_ts, thread_ts (or -), author_id. Escape tabs/newlines in labels to spaces. Write an empty page for a successfully empty query, never omit a required search. Search result IDs and timestamps come from tool responses.
4. Run `python3 <brain>/wiki/maintenance/workflows/scripts/collect_slack.py manifest <work-dir> <brain>/wiki/meta/sources.json`. Pass literal safely quoted paths. Nonzero exit means incomplete/invalid discovery; fix the reported pages before capture completion. The helper dynamically enumerates selected searches/channels and excludes unapproved DMs. No fixed personal IDs or channel counts.
5. Fetch every candidate in `manifest.tsv`, all pages of in-day messages. Preserve the full thread root, the last three replies before the first in-day reply, and every in-day reply. For unthreaded DMs, preserve all day messages and up to three preceding messages within the prior 24 hours. Follow participating replies in older DM threads. Earlier context already on disk may be referenced by stable source ID plus resolvable local path; label the bounded earlier context explicitly. This is not a promise to copy all historical replies.
6. Write scratch day output with capture_status, D, timezone, actual bounds and discovery/capture result. Each block starts `## <title>` and includes `Capture-ID: <manifest id>`, `Participants:`, `Thread:` (original permalink if available, otherwise stable channel/root ID), `Attachments:`, then timestamped original messages with message IDs and resolved names where available. Prefix every source-body line with Markdown `> ` so source headings or metadata-like text cannot masquerade as capture structure; preserve the text after that display prefix verbatim. Include one block per manifest candidate. Never paraphrase messages or replace them with placeholders. Missing/denied full reads block publication.
7. Run `python3 <brain>/wiki/maintenance/workflows/scripts/collect_slack.py check <work-dir> <scratch-day-file>`. This checks structural candidate coverage, not semantic completeness; separately verify full fetch pagination and timestamps. Publish by atomic rename to `raw/inbox/slack/YYYY-MM-DD-slack.md` only when both pass. A complete empty discovery gets an empty-day record. Re-runs compare content, preserve changed prior versions and do not duplicate unchanged output.
8. Persist the stream run record last with exact date/window, source IDs, pagination and completeness. Backfill known missing days oldest-first within configured backfill_days; report older gaps. Archive only fully ingested versions older than active_days, repairing citations under the engine lock or deferring the move. Never delete source material. Release the owned lock and report actual counts/gaps.


## Self-improvement contract

Discovery scope is user-configured and mechanically checked. Full in-day capture plus defined bounded context; explicit coverage and stable IDs. Partial or denied reads never produce complete day-files. Re-runs preserve prior complete output. Archive only ingested material; no deletion or scope expansion.
