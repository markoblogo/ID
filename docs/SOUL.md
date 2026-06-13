# `soul.md`

`profiles/<owner>/soul.md` is the compact, agent-facing working self-model derived from the canonical ID source files.

## Role

- `profile.minimal.md`, `profile.core.md`, and `profile.extended.md` remain the source of truth
- `CHANGELOG.md` contributes recent operational signals
- `soul.md` is the short derived layer meant for fast agent bootstrap

## What belongs in `soul.md`

- stable operational preferences
- working defaults and domain preferences
- repeated misalignments worth preventing
- recent session signals that still matter
- owner-reviewed manual corrections

## What does not belong there

- raw private logs
- speculative psychoanalysis
- hidden inference without provenance
- long archival history that should stay in the source profiles

## Provenance

Generated bullets are tagged:

- `[owner-stated/<source>]` from profile files
- `[recent-session]`, `[recent-change]`, `[open-question]` from `CHANGELOG.md`
- `[derived]` only when source coverage is missing

## Refresh flow

Generate or refresh:

```bash
idctl refresh-soul --owner-id <owner-id>
```

Check for drift without writing:

```bash
idctl refresh-soul --owner-id <owner-id> --check --format json
```

`Manual Corrections` is preserved across refreshes between the `SOUL_MANUAL_START` / `SOUL_MANUAL_END` markers.
