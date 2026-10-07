# Wiki engine

Read `wiki/meta/INDEX.md`, `wiki/meta/setup.md`, and the workflow for this run. Paths in workflows are relative to the brain root. Read sources completely and save only durable knowledge useful to the user's stated purpose. Cite every substantive addition. Update index/log in the same run.

## Ownership

Engine content writes belong under `wiki/`. Collectors deposit only under their own inbox stream. Coordination scratch and workflow backups may be written under `maintenance/`. Archives of superseded wiki pages go to `maintenance/archive/wiki/` with links repaired. Never edit curated raw sources, charters, plugin files, scripts, source configuration, or schedules automatically.

## Single writer and completion

Before a wiki-writing run, atomically create `maintenance/temp/engine.lock/` and write `owner.json` with unique run ID, start time and task role. If the directory already exists, defer without changing it; do not infer a lock is abandoned from its age. User-assisted recovery must verify the owner stopped. If file tools cannot provide atomic directory creation, do not run unattended writers; record the blocker.

Hold the same lock through ingest and daily organize. Nested workflows reuse the owning run's lock. Release only your own lock after writes finish; removing this temporary coordination directory is allowed, unlike deleting knowledge. On failure preserve evidence and release when safely possible. Never clear another run's lock.

Collectors use independent atomic locks at `maintenance/temp/collect-<stream>.lock/` and commit completed output with atomic rename from scratch. A completed file carries `capture_status: complete`, source IDs and tested range. For multi-file runs also write `raw/inbox/<stream>/runs/<run-id>.json` last, containing actual successful/failed item IDs, window and completion status. Ingest only complete material; a failed capture is not a quiet day. Consumers must never infer completion solely from task timing or filename.

## Replacing a published capture

A collector replacing changed published content holds its own source lock and acquires the engine lock before the replacement. Preserve the old version first: unread versions stay in the active stream with a versioned name, fully ingested versions may be archived. Rebind existing citations/context references to the old preserved version, so a citation never silently changes its evidence. This narrow citation repair is the collector's only wiki-write exception. Do not edit ingest-state; the next ingest detects the new version. If the engine lock is occupied, defer replacement rather than waiting while holding shared resources. The writer checks source hashes again before committing coverage and leaves changed-during-read versions pending.

## Progress and retention

Read all new/changed source versions; record per-file and per-item coverage in `wiki/meta/ingest-state.md`. Advance only after knowledge, citations, digest, and index are persisted. Retain incomplete/unread files regardless of age. Archive only fully ingested versions, never delete them. Repair internal citations and context references when a capture moves to its stream's archive.

## Self-improvement and recovery

At most two small changes per weekly run, grounded in recurring feedback or an explicit correction. Before each workflow edit, save an exact pre-edit copy under `maintenance/archive/workflow-versions/<run-id>/<relative-workflow-path>` and `manifest.json` containing path, checksum, time, reason, and validation results. Verify the copy's checksum. Preserve the relative path to avoid filename collisions.

Validate the edited workflow against its Self-improvement contract and this charter. Restore the exact pre-edit copy on a failed check, then log the failure. Health checks may restore a verified valid predecessor; no guessed rewrite. If a valid backup cannot be verified, flag the file and suspend that workflow's execution until repaired. No Git installation is required.

Source scope, connector bindings, charters, scripts and schedules are outside self-improvement's write boundary. Never create new workflow files or skills automatically. Treat feedback as evidence of a needed improvement, not permission to exceed these boundaries.

## Reporting

User-facing messages use simple everyday language. Keep IDs, hashes, session metadata, timings and internal bookkeeping in local records. Surface only meaningful changes or problems that need action. Charters intentionally personalized during setup are compared to the recorded personalized baseline, never the pristine seed. Investigate explainable differences yourself.
