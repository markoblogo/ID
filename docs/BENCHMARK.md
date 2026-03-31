# Benchmark Framework (Phase 5)

## 1. Goal

Create a repeatable comparison framework across AI tools/models for profile alignment quality.

## 2. Core Metrics

- `style_fit` (0-5): how well output matches user communication preferences.
- `constraint_adherence` (0-5): compliance with must/never rules.
- `result_quality` (0-5): usefulness of final artifact.
- `edit_count` (integer): number of user correction turns needed.
- `time_to_acceptable_min` (float): minutes to reach acceptable result.

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

Template for result file:
- `templates/benchmark-result.json`

## 5. Aggregation

Use report script:

```bash
python3 scripts/benchmark_report.py --run-id <run-id>
```

Output:
- `benchmarks/runs/<run-id>/summary.json`
- `benchmarks/runs/<run-id>/summary.md`

## 6. Comparison Policy

- compare tools on the same task set and profile version.
- keep evaluator consistent per run when possible.
- preserve raw evidence in run notes (without sensitive data leakage).

## 7. Minimum Run Metadata

Required in `meta.json`:
- `run_id`
- `date`
- `owner_id`
- `profile_version`
- `tools`
- `evaluator`
