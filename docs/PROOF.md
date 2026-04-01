# Proof

## Goal

Show the strongest current evidence that `ID` improves practical human-AI workflow quality, while keeping scope and caveats explicit.

This page is intentionally short:
- claim
- evidence
- caveat

## Claim 1: `ID` reduces onboarding friction

Current repo-tracked evidence:
- average onboarding latency improvement: `1.15` minutes
- average clarification-turn improvement: `0.85`
- average first-pass success improvement: `0.3`

Primary evidence:
- `benchmarks/runs/public-metrics.md`
- `benchmarks/runs/public-metrics.json`

Interpretation:
- with `ID`, the tested tools needed less setup time and fewer corrective turns before acceptable output

Caveat:
- current control runs are limited and some are synthetic matched controls, not a full external evaluation program

## Claim 2: `ID` improves output quality, not just workflow neatness

Current repo-tracked evidence:
- average task success delta: `0.6`
- average alignment index delta: `18.3`
- average high-alignment-rate delta: `0.6`

Primary evidence:
- `benchmarks/runs/public-metrics.md`
- `docs/EVALUATOR_PROTOCOL.md`

Interpretation:
- the measured gain is not only in speed; the outputs are also closer to the expected style/constraint/result target

Caveat:
- this is benchmark evidence inside the current repo/task set, not a universal claim for all tasks or vendors

## Claim 3: `ID` materially reduces prompt boilerplate

Current repo-tracked evidence:
- average prompt reduction ratio: `0.676`
- average prompt reduction: `607.0` characters

Primary evidence:
- `benchmarks/runs/public-metrics.md`
- `docs/MEASUREMENT.md`

Interpretation:
- the profile and artifact system reduces repeated hand-written context in matched with-vs-without-ID comparisons

Caveat:
- canonical tracked prompt reduction is character-count based for determinism, not tokenizer-native by default

## Claim 4: `ID` is portable with explicit loss boundaries

Current repo-tracked evidence:
- validated artifacts:
  - `profiles/<owner>/interop.v1.json`
  - `profiles/<owner>/context.compact.json`
  - `profiles/<owner>/mcp.context.resource.json`
- import adapters and round-trip loss tests exist
- compatibility and observed-behavior layers are documented

Primary evidence:
- `docs/COMPATIBILITY.md`
- `docs/OBSERVED_BEHAVIOR.md`
- `profiles/markoblogo/interop.v1.json`
- `profiles/markoblogo/context.compact.json`
- `profiles/markoblogo/mcp.context.resource.json`

Interpretation:
- `ID` is not locked to one product memory system; it can move between source markdown, compact transport, and MCP-style transport with documented degradation

Caveat:
- portability is not zero-loss, and import flows currently return reviewable drafts rather than canonical source restoration

## Claim 5: `ID` has explicit trust and privacy boundaries

Current repo-tracked evidence:
- machine-readable privacy policy
- policy-aware compact export
- policy-aware MCP export
- strict validation path covering privacy policy and generated artifacts

Primary evidence:
- `docs/PRIVACY.md`
- `docs/PRIVACY_POLICY_V1.md`
- `docs/THREAT_MODEL.md`
- `profiles/markoblogo/privacy-policy.v1.json`

Interpretation:
- the repo treats privacy and transport loss as protocol concerns, not only as documentation notes

Caveat:
- this is still repo-level trust engineering, not a substitute for vendor-side privacy guarantees

## Current Best Evidence Bundle

If someone wants the shortest credible proof pack, point them to:
- `docs/WHY_ID.md`
- `docs/EXAMPLES.md`
- `docs/MEASUREMENT.md`
- `docs/OBSERVED_BEHAVIOR.md`
- `benchmarks/runs/public-metrics.md`

## What This Does Not Prove

This repo does **not** yet prove that:
- `ID` outperforms every vendor memory feature in every workflow
- current benchmark deltas generalize to every domain
- exports are lossless
- maintenance burden disappears once the protocol exists

## Bottom Line

The strongest current evidence is:
- `ID` reduces repeated onboarding work
- `ID` improves measured task quality inside the repo benchmark setup
- `ID` makes portability, privacy, and degradation more explicit and auditable than prompt-only workflows
