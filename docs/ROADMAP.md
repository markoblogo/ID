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

## Phase 4: Integrations (done)

- unified hook runner added (`scripts/run_integration_hook.sh`);
- ecosystem-specific guides added (`integrations/agentsmd`, `integrations/lab`, `integrations/set`);
- LAB experiment template added (`templates/lab-experiment.md`);
- integration spec updated (`docs/INTEGRATIONS.md`).

## Phase 5: Benchmark + Interop (done)

- benchmark task suite added (`benchmarks/tasks/*`);
- benchmark aggregation script added (`scripts/benchmark_report.py`);
- benchmark result template added (`templates/benchmark-result.json`);
- interop v1 spec and migration guide added (`docs/INTEROP_V1.md`);
- interop schema added (`schemas/interop-v1.schema.json`);
- interop export helper added (`scripts/export_interop_v1.py`).

## Phase 6: Hardening (done)

- CI workflow added (`.github/workflows/ci.yml`) with syntax + guard + validation checks;
- benchmark baseline helpers added (`scripts/benchmark_init_run.py`, `scripts/benchmark_validate_run.py`);
- first baseline benchmark run committed (`benchmarks/runs/baseline-2026-03-31-codex`);
- interop exporter improved to typed mapping with fallback `extensions`;
- interop schema-aligned validator added (`scripts/validate_interop_v1.py`) and wired into CI;
- hardening docs extended with concrete examples and troubleshooting notes.

## Phase 7: Expansion (next)

- add at least one comparative baseline for another tool/model;
- add lightweight trend report across multiple runs;
- formalize evaluator protocol to reduce scoring variance.
