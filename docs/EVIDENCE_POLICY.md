# Evidence Policy

## Goal

Define how evidence-backed claims in `ID` should be maintained over time.

This applies to:
- `docs/OBSERVED_BEHAVIOR.md`
- `docs/PROOF.md`
- `evidence/observed-behavior/*.json`
- benchmark/public metrics used to justify protocol or product claims

## 1. Evidence Classes

### A. Benchmark-derived evidence

Examples:
- `benchmarks/runs/public-metrics.json`
- `benchmarks/runs/public-metrics.md`
- benchmark deltas and prompt-reduction metrics

Use when claiming:
- onboarding improvement
- clarification-turn reduction
- task success / alignment gains
- measurable prompt reduction

### B. Workflow-derived evidence

Examples:
- `evidence/observed-behavior/*.json`
- `docs/OBSERVED_BEHAVIOR.md`

Use when claiming:
- preferred onboarding mode by tool family
- observed degradation patterns
- best current artifact per tool family

## 2. Freshness Rule

Evidence should not be treated as current indefinitely.

Default policy:
- observed-behavior evidence older than `180` days should be treated as stale
- stale evidence should be refreshed, downgraded in confidence, or explicitly scoped as historical

Benchmark artifacts should also be refreshed when:
- benchmark task mix changes materially
- scoring semantics change materially
- transport/export behavior changes in a way that affects claims

## 3. Confidence Update Rules

### Upgrade confidence when

- the same pattern appears across repeated real runs or workflows
- the claim is supported by both artifacts and repeated operator use
- degradation patterns remain stable across more than one task family or tool session

### Downgrade confidence when

- evidence is old and not recently rechecked
- behavior changes after exporter/policy/benchmark updates
- the claim depends on synthetic or narrow evidence only
- observed results differ from the documented recommendation

## 4. Claim Maintenance Rules

Any public claim should be able to point to:
- its primary evidence source
- the date of that evidence
- the main scope limit or caveat

If that cannot be done, the claim should be:
- removed
- weakened
- or clearly labeled as provisional

## 5. Update Triggers

Update evidence when:
- a benchmark delta changes materially
- a preferred artifact changes for a tool family
- new observed degradation appears repeatedly
- confidence level changes
- the protocol/export surface changes in a way that affects prior claims

## 6. Minimal Review Loop

For observed-behavior evidence:
1. re-check whether the note is still current
2. confirm confidence level still matches available evidence
3. confirm cited artifacts/runs still exist
4. update `observed_at` if the note remains current after review

## 7. Validation Posture

Current repo posture:
- structured observed-behavior notes are validated
- evidence date freshness is checked in the validator
- public proof pages should cite benchmark or evidence artifacts directly

Human review is still required for:
- deciding confidence upgrades/downgrades
- deciding whether evidence is representative enough for product claims
- deciding when a stale claim should be retired rather than refreshed
