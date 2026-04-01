# Public Utility Metrics

## Goal

Expose a small, public-facing proof layer for `ID` so benchmark value is visible outside raw evaluator notes.

## Report

Generate the public metrics report with:

```bash
python3 scripts/benchmark_public_report.py
```

Or via the repo shortcut:

```bash
make metrics
```

Outputs:
- `benchmarks/runs/public-metrics.json`
- `benchmarks/runs/public-metrics.md`

## Current Public Metrics

- `onboarding_latency_min`: average minutes to acceptable output across benchmark tasks.
- `clarification_turns_avg`: average number of user correction turns per task.
- `task_success_rate`: share of tasks with `result_quality >= 4` and `constraint_adherence >= 4`.
- `high_alignment_rate`: share of tasks with `style_fit >= 4`, `constraint_adherence >= 4`, and `result_quality >= 4`.
- `first_pass_success_rate`: share of tasks accepted with `edit_count == 0` and success-level quality.
- `alignment_index`: normalized composite of style fit, constraint adherence, and result quality on a 0-100 scale.
- `profile_freshness`: snapshot of current profile staleness based on `updated_at` and `freshness_ttl_days` front matter.

## Not Yet Instrumented

These remain explicit gaps in the public proof layer:
- `prompt_length_reduction`
- `with_vs_without_id_delta`

Both require additional instrumentation and matched control runs, so they are listed in the report but not yet scored.
