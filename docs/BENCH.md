# ID Bench

## Goal

Show whether `ID` is actually useful, not only well-structured.

Use `ID Bench` when you want:
- benchmark runs
- with-vs-without-ID comparisons
- public metrics
- proof that the protocol improves outcomes

## Core Pieces

- benchmark tasks and runs under `benchmarks/`
- `docs/BENCHMARK.md`
- `docs/EVALUATOR_PROTOCOL.md`
- `docs/MEASUREMENT.md`
- `docs/PROOF.md`

## Typical Flow

### 1. Run and validate benchmark artifacts

```bash
make trend
make metrics
```

### 2. Read the public output

- `benchmarks/runs/public-metrics.md`
- `docs/PROOF.md`

### 3. Interpret the result correctly

Use:
- `docs/EVALUATOR_PROTOCOL.md`
- `docs/MEASUREMENT.md`
- `docs/EVIDENCE_POLICY.md`

## Best Use Cases

- proving reduced onboarding friction
- showing fewer clarification turns
- measuring success/alignment delta with and without `ID`
- validating that a profile is not only tidy, but useful

## Current Signals In This Repo

Current public proof includes:
- onboarding latency improvement
- clarification-turn improvement
- task success delta
- alignment index delta
- prompt length reduction

## Caveat

`ID Bench` is still repo-level evidence, not universal external certification.

That is why the repo also keeps:
- observed-behavior notes
- confidence levels
- explicit caveats and scope limits
