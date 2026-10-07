# collect-sessions

Capture full accessible work-session transcripts without collecting the engine's own run logs.

## Read first

Read `.claude/CLAUDE.md`, `wiki/.claude/CLAUDE.md`, `wiki/meta/INDEX.md`, and `wiki/meta/sources.json`. Collectors also read `raw/.claude/CLAUDE.md`. All paths are brain-root-relative. Use configured timezone and actual tested tool bindings, never guessed tool names.

## Zone rule

Write only `raw/inbox/claude-sessions/` and source coordination scratch. Never access an on-disk private session store.

Citation-path repairs during version publication or archival are the narrow wiki-write exception defined in the engine charter; require the engine lock and never change claim meaning or ingest-state.

## Procedure

During user-requested setup, run the connection checks using the onboarding defaults without another scope questionnaire. Sources remain inactive until checked; recurring runs require enabled state and `passed` or `passed_empty` evidence. An incomplete test is remaining work to finish, not a reason to abandon setup. `passed_empty` means access and complete empty discovery were verified; it never asserts a full-body read. Capture boundaries apply to dated streams; all-accessible sessions with no timestamps use stable IDs/version progress instead. Preserve explicit user overrides on resume.


1. Require enabled and verified (`passed` or `passed_empty`) `sources.sessions` and the tested `session_info` list/read capabilities. Acquire the sessions lock. If unavailable, report blocked and leave progress unchanged. Use `scope: all_accessible` by default, including future accessible sessions. Do not require a timestamp or a frozen session-ID allowlist for this scope. Preserve an explicitly narrower user choice when resuming.
2. Enumerate available sessions newest-first through all pages required to establish coverage. Exclude child agents and the engine's `brain-collect-*`, `brain-ingest`, `brain-organize`, `brain-self-improve`, and health-check runs, plus verified pure-refresh automation logs, by actual task role/ID (map friendly scheduled names through the registry); preserve actual user work that discusses the engine. Do not stop after an arbitrary run of known sessions unless ordering/update semantics guarantee no later changed item.
3. Use stable session ID plus reliable last-update/version metadata for idempotency. If the API provides no reliable update version, re-read in-scope sessions needed for coverage and compare content hashes; never assume an idle session cannot later grow. Record that capability/cost limitation explicitly.
4. Read full transcripts from the opening turn, with available full-format/high-limit or paginated reads. Verify beginning/end and all pages. Read complete tool-result spillover files through file tools; if inaccessible, report a tooling gap, never silently truncate. Copy user/assistant turns verbatim; retain connector-provided collapsed tool-call markers. Do not place transcript text into executable shell strings.
5. Write one stable `YYYY-MM-DD-<slug>-<session-id>.md` with session_id, title, status, first_captured, last_updated, source version/hash, message count, source capability and capture_status. For sources without session timestamps, use the actual first-capture date in the configured timezone as the filename date and `first_captured`, keeping it stable on updates. Record source start/end dates as unknown rather than treating capture time as session time. Set `last_updated` to the actual retrieval time and compare content hashes when no source version exists. Measure active retention from the latest captured content change, so an old session updated today remains active until fully ingested. A running session may be retained with `capture_status: incomplete` but is not ingestible. Refetch when settled. Preserve prior settled versions before replacement; unchanged versions produce no write.
6. Publish atomically and record actual run scope and failures. Archive only fully ingested settled versions beyond active_days; retain incomplete sessions. Preserve version-aware coverage and repair citations under the engine lock or defer archiving. Release the owned lock and report captured/changed/skipped/blocked counts.


## Self-improvement contract

Use only tested session_info access and approved scope. Full transcripts, never summaries. Running/partial sessions are not ingestible. Stable IDs and version checks prevent duplicates without skipping changed idle sessions. No private-store scraping, hard deletion, or scope expansion.
