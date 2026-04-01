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

## Prompt Length Reduction

`prompt_length_reduction` is now computed from per-task `prompts/<task-id>.json` payloads in matched `id` and `no_id` runs.

The report measures the average fraction of prompt characters removed by using `ID` instead of repeating the same context manually. Positive values mean the `ID`-backed prompt is shorter.

## Control Runs

To compute `with_vs_without_id_delta`, create matched run pairs with:
- `context_mode`: `id` or `no_id`
- `comparison_group`: shared key for the pair

Positive delta means `ID` performed better. For latency and clarification metrics, the report inverts the sign so positive still means improvement.

## Prompt Payload Capture

Each benchmark run should include `prompts/<task-id>.json` files with four prompt segments:
- `system`
- `profile_context`
- `task_context`
- `task_instruction`

The public metrics layer uses character counts across these segments as a deterministic prompt-size proxy, avoiding tokenizer-specific dependencies.
