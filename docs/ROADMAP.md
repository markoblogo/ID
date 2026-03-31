# ID Roadmap (Draft)

## Phase 0: Bootstrap (done)

- protocol spec drafted;
- operations playbook drafted;
- templates and schemas added.

## Phase 1: Ingest + Extractor MVP (done)

- source ingestion contract added (`docs/INGEST_SOURCES.md`);
- data layers created (`data/raw`, `data/normalized`, `data/processed`);
- extractor MVP added (`scripts/extract_profile.py`).

## Phase 2: Privacy + Redaction (in progress)

- privacy policy added (`docs/PRIVACY.md`);
- redaction script added (`scripts/redact_for_sharing.py`);
- safe-share package template added (`templates/safe-share-package.md`).

## Phase 3: Validation Automation (next)

- add CLI validation for profile metadata freshness;
- add checks against publishing `data/raw/**`;
- add post-session changelog helper.

## Phase 4: Integrations

- `agents.md`: automatic injection of `profile.core.md` at session start;
- `LAB`: experiment registry for prompt/profile variants;
- `SET`: orchestration checks for stale profiles and mandatory changelog update.

## Phase 5: Benchmark + Interop

- add repeatable benchmark tasks across AI tools;
- track style-fit, edit count, and time-to-acceptable-result;
- publish stable `v1` field naming and migration guide.
