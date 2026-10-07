# collect-transcripts

Capture full Zoom transcripts, one stable file per meeting, from recordings and My Notes.

## Read first

Read `.claude/CLAUDE.md`, `wiki/.claude/CLAUDE.md`, `wiki/meta/INDEX.md`, and `wiki/meta/sources.json`. Collectors also read `raw/.claude/CLAUDE.md`. All paths are brain-root-relative. Use configured timezone and actual tested tool bindings, never guessed tool names.

## Zone rule

Write only `raw/inbox/call-transcripts/` and source coordination scratch. Never prune transcripts or modify curated sources.

Citation-path repairs during version publication or archival are the narrow wiki-write exception defined in the engine charter; require the engine lock and never change claim meaning or ingest-state.

## Procedure

During user-requested setup, run the connection checks using the onboarding defaults without another scope questionnaire. Sources remain inactive until checked; recurring runs require enabled state and `passed` or `passed_empty` evidence. An incomplete test is remaining work to finish, not a reason to abandon setup. `passed_empty` means access and complete empty discovery were verified; it never asserts a full-body read. Capture boundaries apply to dated streams; all-accessible sessions with no timestamps use stable IDs/version progress instead. Preserve explicit user overrides on resume.


1. Require enabled and verified (`passed` or `passed_empty`) `sources.transcripts`. Acquire the transcripts source lock. Enumerate both recording and My Notes sources within the configured window (default run day and two previous local days); paginate to exhaustion and use all accessible transcripts by default, including recordings hosted by others. Enforce a narrower own/attended/explicit-meetings scope only if the user explicitly requested it; do not ask during ordinary setup.
2. On missed runs extend the window to close known gaps, capped at configured `backfill_days`; report older gaps. Keep unresolved transcript IDs pending across runs. A missing transcript is not a successfully processed meeting.
3. Match recording and My Notes records using verified meeting IDs/UUIDs when available. Otherwise use overlapping actual meeting time and title only when the match is unambiguous. Never collapse recurring meetings by numeric meeting number alone: key by occurrence UUID or recording start plus meeting number; for notes-only use stable note ID. Record ambiguous duplicates for review.
4. Prefer the complete cloud-recording transcript. If unavailable, fetch the full My Notes transcript including speaker mapping. Use the tested recording-resource/note-content capabilities; tool names are resolved during setup. Never substitute an AI meeting summary for a transcript. Preserve speaker labels and relative timestamps.
5. Handle one meeting from fetch through write before fetching the next. Read full spilled results when available; if inaccessible or truncated, record that precise failure and keep the meeting pending. No empty transcript files. Distinguish permission denied, not found, processing pending, payload inaccessible and genuinely absent transcript.
6. Produce `YYYY-MM-DD-zoom-<title-slug>-<occurrence-id>.md` with capture_status, source ID/occurrence key, meeting/note IDs, title, participants, actual start, duration if available, source URL if returned, retrieval time and transcript completeness. Unknown metadata stays null/unknown, never invented. Body is every utterance with speaker and timestamp. Publish atomically; unchanged completed versions are skipped. Preserve a prior version if a verified transcript correction changes content.
7. Write a run record with enumeration completeness, captured/already-present/pending/blocked occurrence IDs. Only complete individual files are ingestible; a run with pending calls does not imply those calls were captured. Retain transcripts indefinitely and release the owned lock.


## Self-improvement contract

Read both supported transcript sources, within approved scope. Preserve full utterances and speaker mapping. One file per occurrence, not recurring meeting number. Never summarize or fabricate missing transcripts. Never prune. Persist pending IDs and honest completion evidence.
