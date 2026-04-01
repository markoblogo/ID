# ID Protocol

![ID Protocol Logo](images/IDlogo.png)

`ID` is a repository standard for portable human-AI interaction context.

Main idea:
- any AI should quickly understand how to work with a specific person;
- context has depth levels: short, extended, full;
- using context implies responsibility to keep it updated.

## Repository Structure

```text
.
├── benchmarks/
│   ├── tasks/
│   └── runs/
├── data/
│   ├── raw/
│   ├── normalized/
│   └── processed/
├── docs/
│   ├── PROTOCOL.md
│   ├── OPERATIONS.md
│   ├── INGEST_SOURCES.md
│   ├── PRIVACY.md
│   ├── VALIDATION.md
│   ├── INTEGRATIONS.md
│   ├── BENCHMARK.md
│   ├── INTEROP_V1.md
│   ├── HARDENING.md
│   └── ROADMAP.md
├── integrations/
│   ├── agentsmd/
│   ├── lab/
│   └── set/
├── lab/
│   └── experiments/
├── profiles/
├── schemas/
├── scripts/
├── templates/
└── README.md
```

## Phase Status

- Phase 0 (bootstrap): done
- Phase 1 (ingest + extractor MVP): done
- Phase 2 (privacy/redaction): done
- Phase 3 (validation automation): done
- Phase 4 (integrations): done
- Phase 5 (benchmark + interop): done
- Phase 6 (hardening): done
- Phase 7 (expansion): done

## Ecosystem Links

- SET orchestration: https://github.com/markoblogo/SET
- Lab catalog: https://github.com/markoblogo/lab.abvx
- agentsgen toolchain: https://github.com/markoblogo/AGENTS.md_generator

## Ingest + Extract

- put exports to `data/raw/<source>/`
- normalize into `data/normalized/<source>/`
- run: `python3 scripts/extract_profile.py --owner-id <owner-id>`

## Privacy + Safe-Share

- policy: `docs/PRIVACY.md`
- run: `python3 scripts/redact_for_sharing.py`
- review: `data/processed/redaction-report.json`

## Validation + Changelog Automation

- validate: `python3 scripts/validate_profile.py --owner-id <owner-id>`
- publish guard: `python3 scripts/check_publish_guard.py --all-tracked`
- post-session entry:
  - `python3 scripts/session_update.py --owner-id <owner-id> --session-context "..." --sections-used "..." --changes-made "..."`

## Integrations Hooks

- pre-task:
  - `scripts/run_integration_hook.sh pre_task --owner-id <owner-id> --target agentsmd`
- post-task:
  - `scripts/run_integration_hook.sh post_task --owner-id <owner-id> --session-context "..." --sections-used "..." --changes-made "..."`
- weekly review:
  - `scripts/run_integration_hook.sh weekly_review --owner-id <owner-id>`

## Benchmark + Interop

- benchmark guide: `docs/BENCHMARK.md`
- run aggregation: `python3 scripts/benchmark_report.py --run-id <run-id>`
- trend report across runs: `python3 scripts/benchmark_trend_report.py`
- initialize benchmark run: `python3 scripts/benchmark_init_run.py --run-id <run-id> --tool <tool> --owner-id <owner-id> --profile-version <version>`
- validate benchmark run: `python3 scripts/benchmark_validate_run.py --run-id <run-id>`
- interop v1 guide: `docs/INTEROP_V1.md`
- export interop json: `python3 scripts/export_interop_v1.py --owner-id <owner-id>`
- interop artifact policy: `profiles/<owner>/interop.v1.json` is versioned and must be regenerated after profile changes
- validate interop json: `python3 scripts/validate_interop_v1.py --owner-id <owner-id>`

## Hardening

- hardening guide: `docs/HARDENING.md`
- CI workflow: `.github/workflows/ci.yml`
- baseline example: `benchmarks/runs/baseline-2026-03-31-codex/`
