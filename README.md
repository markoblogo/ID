# ID Protocol

![ID Protocol Logo](images/IDlogo.png)

`ID` is a repository standard for portable human-AI interaction context.

Main idea:
- any AI should quickly understand how to work with a specific person;
- context has depth levels: short, extended, full;
- using context implies responsibility to keep it updated.

## Why

Model and tool behavior changes over time. Stable productivity comes from a stable user profile and explicit communication protocol, not from a single model version.

## Core Objects

1. `core profile`:
compact file for quick onboarding (chat, coding agent, image model).

2. `extended profile`:
deeper context for non-trivial collaboration.

3. `full knowledge base`:
repository/wiki-level archive for long-term continuity.

4. `handshake`:
mandatory first-step prompt block that defines how AI should use profile data.

5. `update log`:
change history proving recency and trust level.

## Repository Structure

```text
.
├── data/
│   ├── raw/
│   ├── normalized/
│   └── processed/
├── docs/
│   ├── PROTOCOL.md
│   ├── OPERATIONS.md
│   ├── INTEGRATIONS.md
│   ├── INGEST_SOURCES.md
│   ├── PRIVACY.md
│   └── ROADMAP.md
├── images/
├── profiles/
│   └── <owner>/
├── schemas/
├── scripts/
│   ├── extract_profile.py
│   └── redact_for_sharing.py
├── templates/
│   ├── profile.core.md
│   ├── profile.extended.md
│   ├── agent.handshake.md
│   ├── change-log.md
│   └── safe-share-package.md
└── README.md
```

## Priority Status

- Phase 0 (bootstrap): done
- Phase 1 (ingest + extractor MVP): done
- Phase 2 (privacy/redaction): in progress
- Next: validation automation, adapters, benchmark

## Quick Start

1. Copy `templates/profile.core.md` to `profiles/<person-id>/profile.core.md`.
2. Fill only stable, high-impact preferences first.
3. Copy `templates/agent.handshake.md` to `profiles/<person-id>/handshake.md`.
4. Create `profiles/<person-id>/CHANGELOG.md` from template.
5. When profile is consumed by AI, update freshness section in changelog.

## Ingest + Extract (MVP)

Detailed source flow: `docs/INGEST_SOURCES.md`.

1. Place raw exports in `data/raw/<source>/`.
2. Normalize text/json into `data/normalized/<source>/`.
3. Run extractor:
   - `python3 scripts/extract_profile.py --owner-id <owner-id>`
4. Review generated files:
   - `profiles/<owner-id>/draft.from-exports.md`
   - `profiles/<owner-id>/conflicts.from-exports.md`
5. Merge approved findings into canonical profile files manually.

## Privacy + Safe-Share (MVP)

Policy: `docs/PRIVACY.md`

1. Keep personal exports in `data/raw/` (private only).
2. Redact normalized layer for sharing:
   - `python3 scripts/redact_for_sharing.py`
3. Review `data/processed/redaction-report.json`.
4. Build sharing package using `templates/safe-share-package.md`.

## First Integration Targets

- `agents.md` ecosystem: use `profile.core.md` as default context.
- `LAB`: use `profile.extended.md` for experiments.
- `SET orchestration`: enforce freshness checks and changelog updates.

## Design Principles

- portability over platform lock-in;
- explicitness over hidden memory;
- verifiability over vibes;
- layered depth over one giant context dump.
