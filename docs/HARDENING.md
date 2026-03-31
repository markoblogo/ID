# Hardening Phase

## 1. CI Checks

CI workflow file:
- `.github/workflows/ci.yml`

Current checks:
- Python syntax (`py_compile`)
- Shell syntax (`bash -n`)
- raw-data publish guard
- profile validation

## 2. Benchmark Baseline Scaffolding

Initialize a benchmark run:

```bash
python3 scripts/benchmark_init_run.py \
  --run-id baseline-2026-03-31-codex \
  --tool codex \
  --owner-id markoblogo \
  --profile-version 0.1.0
```

Validate run completeness:

```bash
python3 scripts/benchmark_validate_run.py --run-id baseline-2026-03-31-codex
```

Aggregate report:

```bash
python3 scripts/benchmark_report.py --run-id baseline-2026-03-31-codex
```

## 3. Interop Export Hardening

`export_interop_v1.py` now uses typed section mapping:
- core: communication, rules, quality_bar, priority_domains, tool_notes
- extended: stable_preferences, misalignments, heuristics, etc.

Unknown headings are preserved under `extensions`.
