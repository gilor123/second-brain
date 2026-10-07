# Ingestion state

No sources processed yet. Record a file content hash or reliable source version, not a timestamp-only guess. Each item carries its stable source ID and completed/pending/blocked state. A latest-date watermark never skips an unfinished earlier item.

| Source/file | Version/hash | Item ID | State | Result/pages or below-bar reason | Completed at |
|---|---|---|---|---|---|
