# Public Utility Metrics

## Goal

Expose a small, public-facing proof layer for `ID` so benchmark value is visible outside raw evaluator notes.

## Report

Generate the canonical public metrics report with:

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

`prompt_length_reduction` is computed from per-task `prompts/<task-id>.json` payloads in matched `id` and `no_id` runs.

The canonical benchmark artifact uses character counts across prompt segments as a deterministic prompt-size proxy. Positive values mean the `ID`-backed prompt is shorter.

## Optional Tokenizer-Aware Layer

You can add a tokenizer-aware prompt-size layer locally without changing the canonical deterministic baseline.

Canonical command:

```bash
make metrics-tokenizer
```

Equivalent direct call:

```bash
python3 scripts/benchmark_public_report.py --tokenizer-provider tiktoken --tokenizer-encoding cl100k_base
```

Properties:
- opt-in only: default `make metrics` does not depend on any tokenizer package
- safe for CI/history: tracked benchmark artifacts should continue to be generated without tokenizer flags
- additive only: tokenizer-aware metrics sit next to the char-count proxy, not instead of it

If `tiktoken` is requested explicitly and not installed, the script fails with a clear error.

## Recommended Tokenizer Conventions

To keep local tokenizer-aware comparisons comparable across runs, fix one tokenizer convention per tool family and keep it stable inside a comparison set.

Recommended defaults:
- OpenAI GPT-family tools: `--tokenizer-provider tiktoken --tokenizer-encoding cl100k_base`
- Claude-family tools: `--tokenizer-provider tiktoken --tokenizer-encoding cl100k_base`
- Gemini-family tools: `--tokenizer-provider tiktoken --tokenizer-encoding cl100k_base`
- Mixed-tool comparisons: use the same tokenizer setting for every run in that comparison group and record it in notes

Operational rules:
- treat tokenizer-aware metrics as secondary local instrumentation, not canonical benchmark artifacts
- do not switch tokenizer settings inside the same `comparison_group`
- prefer `--tokenizer-model` only when the whole comparison set is tied to that exact model mapping
- if model-specific tokenization is uncertain or unstable, fall back to `cl100k_base` for comparability

The char-count proxy remains the canonical tracked baseline because it is deterministic and does not depend on external tokenizer packages or model-mapping changes.

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

The public metrics layer uses character counts across these segments as a deterministic prompt-size proxy, avoiding tokenizer-specific dependencies in canonical artifacts.
