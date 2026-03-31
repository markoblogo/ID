# ID Roadmap (Draft)

## Phase 0: Bootstrap (done)

- protocol spec drafted;
- operations playbook drafted;
- templates and schemas added.

## Phase 1: Ingest + Extractor MVP (done)

- source ingestion contract added (`docs/INGEST_SOURCES.md`);
- data layers created (`data/raw`, `data/normalized`, `data/processed`);
- extractor MVP added (`scripts/extract_profile.py`).

## Phase 2: Privacy + Redaction (done)

- privacy policy added (`docs/PRIVACY.md`);
- redaction script added (`scripts/redact_for_sharing.py`);
- safe-share package template added (`templates/safe-share-package.md`).

## Phase 3: Validation Automation (done)

- profile validator added (`scripts/validate_profile.py`);
- raw publish guard added (`scripts/check_publish_guard.py`);
- post-session changelog helper added (`scripts/session_update.py`);
- usage doc added (`docs/VALIDATION.md`).

## Phase 4: Integrations (next)

- `agents.md`: automatic injection of `profile.core.md` at session start;
- `LAB`: experiment registry for prompt/profile variants;
- `SET`: orchestration checks for stale profiles and mandatory changelog update.

## Phase 5: Benchmark + Interop

- add repeatable benchmark tasks across AI tools;
- track style-fit, edit count, and time-to-acceptable-result;
- publish stable `v1` field naming and migration guide.
