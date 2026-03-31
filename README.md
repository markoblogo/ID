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
│   └── ROADMAP.md
├── profiles/
│   └── <owner>/
├── schemas/
├── scripts/
│   └── extract_profile.py
├── templates/
└── README.md
```

## Priority Status

- Phase 0 (bootstrap): done
- Phase 1 (ingest + extractor MVP): in progress (MVP scaffold added)
- Next: privacy/redaction, validation automation, adapters, benchmark

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

## First Integration Targets

- `agents.md` ecosystem: use `profile.core.md` as default context.
- `LAB`: use `profile.extended.md` for experiments.
- `SET orchestration`: enforce freshness checks and changelog updates.

## Design Principles

- portability over platform lock-in;
- explicitness over hidden memory;
- verifiability over vibes;
- layered depth over one giant context dump.
