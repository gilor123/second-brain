# Page shapes

Use one stable lowercase-hyphenated filename per durable concept or entity. Prefer strengthening an existing page over creating a thin fragment. Every substantive claim must trace to a source with date, original identity, and local path or URL.

Topic/entity shape:

```markdown
---
title: Human-readable title
type: topic
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# Title
## Summary
One to three lines answering what this is.
## Body
Current understanding, with source references next to claims. Flag [uncertain: ...] and [contradiction: source/date says X; source/date says Y].
## Related
Relative links to related pages with a reason for each relationship.
## Sources
Source IDs, dates, and resolvable local/original links.
## Last updated
Date and one line describing the last substantive update.
```

For an entity set `type: entity`; add a useful entity type only when supported. Never promote an unconfirmed model draft into a user decision. Preserve who said what and when.

Daily digest `wiki/digests/YYYY-MM-DD.md`: What changed; New pages; Updated pages; Open questions/contradictions; Coverage (file/version, items read, saved or below bar, blocked); Process feedback. Weekly digest `YYYY-Www.md`: cross-week synthesis and unresolved issues. Counts come from actual coverage, not estimates. An unresolved question may live in `wiki/topics/open-questions.md`; create it only when needed and remove resolved entries while keeping the resolution in the relevant topic and log.
