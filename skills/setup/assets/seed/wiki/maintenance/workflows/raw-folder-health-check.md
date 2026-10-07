# raw-folder-health-check

Review source inventory and source quality weekly without rewriting curated material.

## Read first

Read `.claude/CLAUDE.md`, `wiki/.claude/CLAUDE.md`, `wiki/meta/INDEX.md`, and `wiki/meta/sources.json`. Collectors also read `raw/.claude/CLAUDE.md`. All paths are brain-root-relative. Use configured timezone and actual tested tool bindings, never guessed tool names.

## Zone rule

Read raw and maintenance scratch. Write findings under wiki and the engine lock only. No changes to curated raw or upstream services; archival proposals require user direction.

## Procedure


1. Acquire the engine lock. Compare the source catalog to files in `raw/sources/`: missing files, uncataloged additions, duplicate candidates, unreadable formats and broken original/local references. Distinguish a failed remote permission check from an actually deleted document.
2. Compare source versions and citations where evidence is available. Flag potentially stale snapshots or conflicting sources; do not refresh Drive, change a document, or rewrite a source index automatically. Initial import is separate from ongoing mirroring.
3. Inspect `maintenance/temp/` for completed scratch candidates. Propose archival paths; do not move active locks, partial collections, or unread sources. Never reorganize collector-owned inboxes.
4. Write/merge `wiki/digests/YYYY-Www-raw-health-check.md` with exact paths, evidence and recommended user action. Keep this distinct from the wiki health report. Update INDEX/log and release the owned lock.


## Self-improvement contract

Read-only source audit. Findings/proposals only, no raw edits or upstream publishing. No Notion or Help Center integration. Never touch active scratch, delete content or report unread material as healthy.
