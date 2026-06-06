# Proof

## Why this evidence exists

This section proves two things:
- `ID` produces measurable workflow improvements where the same task set is run with and without it;
- those gains are bounded by explicit trust, loss, and portability caveats.

## Claim Pack

### 1) Faster first pass onboarding

`ID` reduces onboarding friction for the same tasks.

- Evidence: `benchmarks/runs/public-metrics.md` and `.json`
- Measured in repo benchmarks: average onboarding latency and clarification turns
- Interpretation:
  - `-1.15` minutes onboarding latency means less setup before first useful output
  - `-0.85` clarification turns means fewer hand-offs to correct context drift

### 2) Better output alignment after repeated interactions

`ID` shifts score mix toward style/constraint compliance in matched task families.

- Evidence: `benchmarks/runs/public-metrics.md`
- Metrics:
  - task success, alignment index, high alignment rate
- Interpretation:
  - output quality is not just “same as before with cleaner wrapping,” it is measurably closer to the profile target in this corpus

### 3) Less repeated prompt boilerplate

`ID` artifacts remove repeated context narration from task prompts.

- Evidence: `benchmarks/runs/public-metrics.md`, `docs/MEASUREMENT.md`
- Interpretation:
  - prompt reduction in this corpus is primarily from stable, reusable context surfaces instead of re-typing constraints every run

### 4) Portability with explicit loss

`ID` is not a fixed memory store. It is a portability layer with known degradations.

- Evidence: `profiles/markoblogo/interop.v1.json`, `profiles/markoblogo/context.compact.json`, `profiles/markoblogo/mcp.context.resource.json`
- Interpretation:
  - portability is explicit and measurable, and imports/exports are validated against documented rules

### 5) Verifiable trust boundaries

`ID` keeps privacy and transport assumptions as data, not only prose.

- Evidence: `docs/PRIVACY.md`, `docs/PRIVACY_POLICY_V1.md`, `docs/THREAT_MODEL.md`, `profiles/markoblogo/privacy-policy.v1.json`
- Interpretation:
  - policy flags influence generated artifacts and tool behavior where it is implemented

## Evidence Surface

- Public metrics: `benchmarks/runs/public-metrics.md` and `benchmarks/runs/public-metrics.json`
- Benchmark protocol: `docs/MEASUREMENT.md`, `docs/EVALUATOR_PROTOCOL.md`
- Compatibility expectations: `docs/COMPATIBILITY.md`
- Conformance intent: `spec/CONFORMANCE.md`

## Non-Claims

Current evidence does **not** claim:
- universal superiority across all providers or tasks;
- zero-loss import/export in all directions;
- complete vendor-side privacy guarantees.

Those areas are tracked in `docs/EVIDENCE_POLICY.md` and update notes.
