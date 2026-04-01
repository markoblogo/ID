# Benchmark Framework

## 1. Goal

Create a repeatable comparison framework across AI tools/models for profile alignment quality.

## 2. Core Metrics

- `style_fit` (0-5): how well output matches user communication preferences.
- `constraint_adherence` (0-5): compliance with must/never rules.
- `result_quality` (0-5): usefulness of final artifact.
- `edit_count` (float/int): number of user correction turns needed.
- `time_to_acceptable_min` (float): minutes to reach acceptable result.

Scoring protocol:
- use `docs/EVALUATOR_PROTOCOL.md` for the shared rubric, calibration flow, confidence, and uncertainty conventions.

## 3. Task Set

Canonical tasks live in `benchmarks/tasks/`.

MVP set covers:
- coding/automation
- structured writing
- data transformation
- agent orchestration
- image/video brief quality

## 4. Run Structure

Create run folder per benchmark execution:

- `benchmarks/runs/<run-id>/meta.json`
- `benchmarks/runs/<run-id>/results/<task-id>.json`
- `benchmarks/runs/<run-id>/notes.md`
- `benchmarks/runs/<run-id>/summary.json`
- `benchmarks/runs/<run-id>/summary.md`

Template for result file:
- `templates/benchmark-result.json`

Recommended per-result fields in addition to numeric metrics:
- `confidence`
- `uncertainty_notes`
- `evidence_links`
- `notes`

## 5. Aggregation

Per-run summary:

```bash
python3 scripts/benchmark_report.py --run-id <run-id>
```

Cross-run trend summary:

```bash
python3 scripts/benchmark_trend_report.py
```

Outputs:
- `benchmarks/runs/trends.json`
- `benchmarks/runs/trends.md`
- `benchmarks/runs/public-metrics.json`
- `benchmarks/runs/public-metrics.md`

## 6. Comparison Policy

- compare tools on the same task set and profile version whenever possible.
- keep evaluator consistent per run when possible.
- preserve run notes and evidence without sensitive data leakage.
- do not compare small score deltas without checking evaluator confidence and evidence quality.

## 7. Minimum Run Metadata

Required in `meta.json`:
- `run_id`
- `date`
- `owner_id`
- `profile_version`
- `tools`
- `evaluator`
- `context_mode`: `id|no_id`

Optional in `meta.json` for control-run comparisons:
- `comparison_group`: shared key between an `id` run and a `no_id` run

Recommended in each task result:
- `confidence`: `high|medium|low`
- `uncertainty_notes`: list of scoring caveats
- `evidence_links`: list of repo-relative paths or stable URLs

## 8. Public Utility Layer

Use the public utility layer to expose benchmark value in product-facing terms rather than only raw evaluator averages.

Primary entrypoints:
- guide: `docs/MEASUREMENT.md`
- report generator: `python3 scripts/benchmark_public_report.py`
- shortcut: `make metrics`

Current public signals:
- onboarding latency
- clarification turns
- task success rate
- high alignment rate
- first-pass success rate
- profile freshness snapshot

Not yet instrumented but explicitly tracked:
- prompt length reduction
- with-vs-without-ID delta
