# Hardening Phase

## 1. CI Checks

CI workflow file:
- `.github/workflows/ci.yml`

Current checks:
- Python syntax (`py_compile`)
- unit tests (`unittest`)
- Shell syntax (`bash -n`)
- raw-data publish guard
- profile validation
- interop export + schema-aligned validation
- trend artifact generation
- drift enforcement for `profiles/*/interop.v1.json` and `benchmarks/runs/trends.*`

## 2. Interop Validation Commands

Generate interop output:

```bash
python3 scripts/export_interop_v1.py --owner-id markoblogo
```

Validate generated file:

```bash
python3 scripts/validate_interop_v1.py --owner-id markoblogo
```

Shortcut:

```bash
make interop
```

Validate explicit file path:

```bash
python3 scripts/validate_interop_v1.py --input profiles/markoblogo/interop.v1.json
```

## 3. Benchmark Baseline Scaffolding

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

Cross-run trends:

```bash
make trend
```

Full local validation path:

```bash
make validate
make drift-check
```

Committed baseline artifacts:
- `benchmarks/runs/baseline-2026-03-31-codex/meta.json`
- `benchmarks/runs/baseline-2026-03-31-codex/results/*.json`
- `benchmarks/runs/baseline-2026-03-31-codex/summary.json`
- `benchmarks/runs/baseline-2026-03-31-codex/summary.md`

## 4. Example Artifacts (Baseline)

Example task result (`task-09-image-brief`):

```json
{
  "task_id": "task-09-image-brief",
  "tool": "codex",
  "style_fit": 3,
  "constraint_adherence": 4,
  "result_quality": 3,
  "edit_count": 2,
  "time_to_acceptable_min": 7,
  "notes": "weaker alignment vs coding workflows"
}
```

Example summary:

```json
{
  "run_id": "baseline-2026-03-31-codex",
  "tasks": 10,
  "averages": {
    "style_fit": 4.2,
    "constraint_adherence": 4.9,
    "result_quality": 4.2,
    "edit_count": 0.8,
    "time_to_acceptable_min": 4.3
  }
}
```

## 5. Troubleshooting

- `python scripts/check_publish_guard.py --all-tracked` fails with raw file paths:
  - ensure no `data/raw/**` files are tracked by git;
  - untrack them and keep only normalized/processed outputs in commits.
- `validate_interop_v1.py` reports missing fields:
  - regenerate file via `export_interop_v1.py`;
  - verify profile front matter keeps required fields (`version`, `updated_at`, etc.).
- benchmark run validation fails (`missing result files`):
  - run `benchmark_init_run.py` for the same `--run-id`;
  - ensure all task files under `benchmarks/tasks/` have corresponding `results/*.json`.
- CI fails while local shell looked fine:
  - rerun exact CI commands locally in the same order from `.github/workflows/ci.yml`;
  - check executable bit for scripts that are invoked directly.
- push hangs in current local environment:
  - use standard `git push origin main` first;
  - if environment issue persists, sync via approved GitHub API fallback process.
- local exec sessions look stuck (no output for simple commands):
  - run `bash scripts/cleanup_stuck_jobs.sh`;
  - then rerun checks one by one (avoid large chained commands while recovering);
  - prefer short commands with explicit timeouts for network checks.

## 6. Interop Export Hardening

`export_interop_v1.py` uses typed section mapping:
- core: communication, rules, quality_bar, priority_domains, tool_notes
- extended: stable_preferences, misalignments, heuristics, etc.

Unknown headings are preserved under `extensions`.
