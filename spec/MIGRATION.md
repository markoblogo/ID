# Profile Migration Guide

## Scope

This guide covers profile front matter metadata migration used by `scripts/migrate.py`.

## Supported Versions

- `v0.1` → `v0.2`
- Same-version no-op
- `v0.2` → `v0.3` and higher (future extension points only)

## v0.1 → v0.2

`v0.2` migration adds metadata fields required for stricter freshness and trust handling:

- `owner_alias` (fallback to `owner_id`)
- `trust_level` (`trusted` if missing)
- `created_at` / `updated_at` timestamps
- `freshness_ttl_days` (default `14`)
- semantic profile `version` normalization to at least `0.2.0`

## CLI Guide

```bash
python3 scripts/migrate.py --owner-id <owner-id> --from v0.1 --to v0.2
```

Dry run:

```bash
python3 scripts/migrate.py --owner-id <owner-id> --from v0.1 --to v0.2 --dry-run --json
```

`--dry-run --json` is recommended in CI or automation before writing files.

## Makefile Targets

- `make migrate OWNER_ID=<owner-id> FROM=v0.1 TO=v0.2 [DRY_RUN=1]`
- `make migrate-check OWNER_ID=<owner-id> FROM=v0.1 TO=v0.2`

## Breaking vs Non-Breaking

- Non-breaking: adding missing metadata fields or setting defaults.
- Potentially breaking: explicit semantics changes to `version`/`updated_at` in generated diffs.

## Version Semantics

Profile semantics continue to live in:

- `profiles/<owner>/profile.core.md`
- `profiles/<owner>/profile.extended.md`

Generated artifacts remain derived outputs and must be regenerated after migration-backed profile updates.
