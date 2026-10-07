# organize

Keep the derived wiki coherent after ingestion and in a deeper weekly pass.

## Read first

Read `.claude/CLAUDE.md`, `wiki/.claude/CLAUDE.md`, `wiki/meta/INDEX.md`, and `wiki/meta/sources.json`. Collectors also read `raw/.claude/CLAUDE.md`. All paths are brain-root-relative. Use configured timezone and actual tested tool bindings, never guessed tool names.

## Zone rule

Read sources for verification; write only wiki plus coordination scratch and archived superseded wiki pages. Never change curated raw.

## Procedure


1. Reuse the ingest writer lock when called from ingest; otherwise acquire it. Read page shapes and the incoming coverage/touched-page list. Standalone weekly work derives its scope from actual pages/logs and states missing coverage instead of inventing counts.
2. Cross-link related topics/entities in both directions with a meaningful reason. Consolidate duplicates into a stable canonical page without dropping supported knowledge. Move superseded pages to `maintenance/archive/wiki/<run-id>/`, repair inbound links and log the move. Do not hard-delete.
3. Surface contradictions and stale claims with evidence. Resolve only when authoritative evidence clearly establishes the answer; preserve the decision in the log and cite it on the topic. Never choose solely by recency.
4. Update `wiki/meta/INDEX.md` for all new/moved pages. Write or merge the daily digest at `wiki/digests/YYYY-MM-DD.md` using stable run IDs; a rerun does not duplicate entries or overwrite earlier same-day coverage. Include actual coverage, pending gaps and process feedback. Append one log entry for the completed run. Do not mark ingest state here; ingestion commits it after this pass succeeds.
5. Weekly mode also checks orphan/near-duplicate topics across the wiki, produces `YYYY-Www.md` and highlights unresolved issues worth user attention. No new facts without source verification. Release the lock only if this invocation acquired it.


## Self-improvement contract

Maintain index, evidence and meaningful bidirectional links. Preserve same-day digests across runs. Archive rather than delete. Separate supported resolutions from unresolved contradictions. Never change raw or collection settings.
