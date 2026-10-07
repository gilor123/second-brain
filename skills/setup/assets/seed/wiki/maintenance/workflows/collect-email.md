# collect-email

Capture relevant Gmail messages as one complete file per calendar day; preserve content and provenance for later synthesis.

## Read first

Read `.claude/CLAUDE.md`, `wiki/.claude/CLAUDE.md`, `wiki/meta/INDEX.md`, and `wiki/meta/sources.json`. Collectors also read `raw/.claude/CLAUDE.md`. All paths are brain-root-relative. Use configured timezone and actual tested tool bindings, never guessed tool names.

## Zone rule

Write only `raw/inbox/email/` and this collector's coordination scratch under `maintenance/temp/`. Never change curated sources or synthesize knowledge.

Citation-path repairs during version publication or archival are the narrow wiki-write exception defined in the engine charter; require the engine lock and never change claim meaning or ingest-state.

## Procedure

During user-requested setup, run the connection checks using the onboarding defaults without another scope questionnaire. Sources remain inactive until checked; recurring runs require enabled state and `passed` or `passed_empty` evidence. An incomplete test is remaining work to finish, not a reason to abandon setup. `passed_empty` means access and complete empty discovery were verified; it never asserts a full-body read. Capture boundaries apply to dated streams; all-accessible sessions with no timestamps use stable IDs/version progress instead. Preserve explicit user overrides on resume.


1. Require `sources.email.status` enabled and verified test evidence (`passed` or `passed_empty`). Acquire the email source lock. Verify Gmail search, full-thread read and pagination through the tested bindings. Resolve the previous full day D in the named timezone using exact UTC start/end instants. Search broadly enough for the timezone boundary and recheck message timestamps locally; Gmail date-string semantics alone are not a boundary guarantee.
2. Collect missing days since the latest completed run, oldest first, capped by `backfill_days`. Record older gaps. Respect the configured capture-start boundary; do not backfill before it. A source's first run captures only its requested window.
3. When `capture_all_mail` is true (new-setup default), search all accessible messages within the window, including sent/received, archived, read/unread, bulk and automated categories; omit spam, trash and drafts. Do not restrict by labels or require label discovery. Read complete threads and recheck each message timestamp, preserving every in-window message within that mailbox scope. If the user explicitly narrowed collection, apply those recorded inclusions/exclusions instead. Use actual supported Gmail operators and paginate to exhaustion; thread-level matches alone are insufficient.
4. Remove duplicated quoted reply chains and signatures conservatively; preserve the new message verbatim. Do not summarize. If cleaning would remove substantive text, retain it. Note attachments with filename/type and whether contents were requested; do not download unrelated attachments.
5. Write scratch output with header `capture_status: complete`, captured day, timezone, actual coverage bounds and source IDs. Per thread use subject, participants, date, labels, matched selection class (`all-mail` by default), original permalink, message ID, and one timestamped body per message. Never invent a permalink; retain connector ID if one is unavailable. A genuinely empty completed search produces an explicit empty-day record.
6. Any missing page/read is an incomplete run: keep scratch and failure evidence, do not publish a complete day-file or advance progress. Preserve a previously complete file on failed re-runs. When complete, atomically publish `raw/inbox/email/YYYY-MM-DD-email.md`, keyed by captured day. Before publishing a changed complete version, acquire the engine lock as well as the source lock. Preserve the old version under a versioned filename in the active stream if it is unread, or in the stream archive if fully ingested. Under the engine lock, rebind citations/context references to that preserved version, then publish the new version. Never edit ingest-state from a collector: ingest detects the new content hash and retains old version coverage. If the engine lock is busy, leave the proposed replacement in scratch and defer publication; unchanged output is a no-op.
7. Record run evidence under the stream's `runs/` directory last. Archive only older-than-`active_days` versions explicitly marked fully ingested. Keep unresolved/unread material active. Repair internal links under the engine lock if archiving changes referenced paths; otherwise defer archiving. Release only your own source lock and report captured/empty/blocked day counts.


## Self-improvement contract

Capture complete in-scope messages with IDs and provenance; exclusions win. No snippets as full bodies. No complete marker on partial input. Re-runs are idempotent; only fully ingested material is archived, never deleted. Source configuration and scope remain unchanged.
