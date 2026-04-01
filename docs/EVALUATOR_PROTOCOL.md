# Evaluator Protocol v0.1

## 1. Goal

Reduce manual scorer drift in benchmark runs by standardizing:

- score meanings;
- evidence expectations;
- confidence and uncertainty reporting;
- evaluator calibration steps.

This protocol applies to result files under `benchmarks/runs/<run-id>/results/*.json`
and complements the benchmark framework in `docs/BENCHMARK.md`.

## 2. Evaluation Flow

For each benchmark task result:

1. read the target task and the relevant profile context;
2. review the final delivered output, not intermediate drafts alone;
3. score the required metrics using the rubric below;
4. attach concise rationale for non-obvious scores;
5. record evaluator confidence and uncertainty notes;
6. attach evidence links or evidence references for later audit.

If a score cannot be justified from saved artifacts, lower confidence and note the gap.

## 3. Required Metrics

Each result keeps these numeric metrics:

- `style_fit`
- `constraint_adherence`
- `result_quality`
- `edit_count`
- `time_to_acceptable_min`

The first three use a `0-5` rubric. The last two are observed process metrics.

## 4. Rubric (0-5)

### `style_fit`

- `0`: actively mismatched tone/format; ignores core communication preferences.
- `1`: major mismatch; heavy rewriting needed before usable.
- `2`: partially aligned but persistent friction in tone, structure, or brevity.
- `3`: acceptable alignment; noticeable but non-fatal mismatch remains.
- `4`: strong alignment; only minor edits needed for style polish.
- `5`: near-native fit for the owner profile and task context.

### `constraint_adherence`

- `0`: violates critical must/never rules.
- `1`: multiple important rule breaks or unsafe assumptions.
- `2`: one major or several moderate adherence problems.
- `3`: mostly compliant; minor misses do not break task safety.
- `4`: strong compliance; only small edge-case misses.
- `5`: fully compliant with explicit constraints and obvious boundary conditions.

### `result_quality`

- `0`: unusable or wrong outcome.
- `1`: major rework required before it can serve the task.
- `2`: weak result; partial utility but substantial repair required.
- `3`: acceptable result; useful with moderate edits.
- `4`: strong result; small edits or verification only.
- `5`: excellent result; directly usable and materially helpful.

## 5. Process Metrics

### `edit_count`

- Count user correction turns needed to reach an acceptable result.
- Count only meaningful corrective turns.
- Do not count neutral acknowledgements, logistics, or repeated retries caused by tooling failures alone.

### `time_to_acceptable_min`

- Measure minutes from first task prompt to the first acceptable result.
- Round to one decimal place when needed.
- If exact time is unavailable, estimate conservatively and document that estimate in `uncertainty_notes`.

## 6. Confidence and Uncertainty

Each task result should include:

- `confidence`: `high`, `medium`, or `low`
- `uncertainty_notes`: list of concrete limitations in scoring confidence

Recommended meaning:

- `high`: evaluator had complete artifacts, clear task success criteria, and low ambiguity.
- `medium`: small evidence gaps or borderline rubric interpretation.
- `low`: missing artifacts, partial memory-based scoring, or strong ambiguity.

Low confidence does not invalidate a run, but it must be explicit.

## 7. Evidence Links

Each task result should include `evidence_links`, a list of strings pointing to:

- stored transcripts;
- saved output artifacts;
- notes files;
- screenshots or attachments;
- commit / PR references where relevant.

Use repo-relative paths or stable URLs whenever possible.

If sensitive evidence cannot be committed, record a short placeholder reference in
`notes` and mention the redaction or storage limitation in `uncertainty_notes`.

## 8. Calibration Rules

Before scoring a run:

- use the same rubric version across all tasks in that run;
- compare against at least one previously scored example when possible;
- avoid changing score standards mid-run;
- keep the same evaluator for all tasks in a run when possible.

If evaluator or rubric changes across runs, note it in run metadata or notes.

## 9. Tie-Break and Interpretation Rules

When comparing runs:

- prioritize `constraint_adherence` over `style_fit` when safety or hard rules are involved;
- prioritize `result_quality` over `style_fit` when style is weaker but task utility is clearly higher;
- use `edit_count` and `time_to_acceptable_min` as efficiency signals, not as substitutes for quality;
- do not over-interpret small deltas without considering confidence and task mix.

## 10. Suggested Result Shape

Recommended benchmark result JSON fields:

```json
{
  "task_id": "task-01",
  "tool": "codex",
  "style_fit": 4,
  "constraint_adherence": 5,
  "result_quality": 4,
  "edit_count": 1,
  "time_to_acceptable_min": 3.5,
  "confidence": "medium",
  "uncertainty_notes": [],
  "evidence_links": [],
  "notes": "minor style compression needed"
}
```

## 11. Non-Goals

- This protocol does not claim objective truth for subjective scores.
- This protocol does not replace artifact review.
- This protocol does not force statistical confidence intervals when the benchmark is still manually evaluated.
