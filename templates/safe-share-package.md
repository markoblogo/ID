# Safe-Share Package Template

Use this checklist before sharing profile context externally.

## Include

- protocol docs (`docs/PROTOCOL.md`, `docs/OPERATIONS.md`)
- redacted profile summary
- interaction rules and workflow preferences
- redaction report from `data/processed/redaction-report.json`

## Exclude

- `data/raw/**`
- unredacted `data/normalized/**`
- private identifiers not required for collaboration

## Optional Evidence Block

If evidence snippets are included, ensure they contain only redacted placeholders.
