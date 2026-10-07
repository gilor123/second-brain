# Source ownership

Read `raw/meta/index.md` to find curated documents. Files in `raw/sources/` are preserved source snapshots, not generated wiki pages. User-directed setup/import may add selected documents and index entries. Recurring ingestion and health checks never edit them.

Collectors may deposit complete captures in their own `raw/inbox/<stream>/` directory, maintain source-specific state there, and archive fully ingested old captures. They do not write curated sources, change their scope, or delete content. A captured assertion is evidence with an author/date, not automatically established truth.

Report proposed source corrections for the user to review. Do not edit upstream documents, publish mirrors, or silently refresh a curated snapshot. Preserve original and retrieved source locations so derived claims can be checked.
