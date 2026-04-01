# Conformance Model

`ID` implementations do not all need to support the same surface area.

Conformance is a claim about demonstrated capability, not intent alone.

## Conformance Levels

### Level 1: Reader

Can:
- read profile markdown;
- follow handshake expectations;
- respect freshness and trust semantics in outputs.

Cannot assume:
- interop export;
- redaction tooling;
- benchmark support.

Minimum claim basis:
- can point to the markdown source it consumes
- can describe how handshake, freshness, and trust semantics are surfaced in operation
- does not silently ignore these semantics while still claiming Level 1

### Level 2: Portable

Includes Level 1, plus:
- export or consume `interop.v1.json`;
- preserve unknown fields or extensions safely;
- document any lossy mapping behavior.

Minimum claim basis:
- validator-backed or otherwise verifiable handling of `interop.v1.json`
- explicit source/target statement
- explicit loss notes or degradation statement
- no silent field dropping for unknown extensions

### Level 3: Privacy-Aware

Includes Level 2, plus:
- support redaction or permission-aware sharing;
- distinguish local-only vs shareable context where possible;
- expose privacy limitations clearly.

Minimum claim basis:
- explicit privacy or policy surface
- demonstrable handling of shareability boundaries
- clear statement of what is not protected or not enforced
- evidence that privacy-aware behavior affects export or sharing behavior, not just prose documentation

### Level 4: Measurable

Includes Level 3, plus:
- support benchmark task execution or benchmark result consumption;
- preserve evidence references;
- emit data suitable for trend comparison.

Minimum claim basis:
- benchmark artifacts or comparable measurable outputs
- preserved evidence references
- repeatable comparison path
- explicit caveats for synthetic controls, limited coverage, or non-generalizable claims

## Claim Hardening Rules

To claim a conformance level, an implementation should provide:
- the claimed level
- source format used
- target format used
- validators or checks that support the claim
- known loss boundaries
- known non-goals or unsupported behaviors

Intent alone is not enough.

A claim is weak if it relies only on:
- prose compatibility guidance without generated artifacts
- exporter output without validation
- one-off examples without repeatable checks
- observed behavior notes without any structured evidence or artifact references

## Evidence Expectations By Level

### Level 1

Expected evidence:
- source markdown reference
- explicit operational description of handshake/freshness/trust handling

### Level 2

Expected evidence:
- generated or consumed interop artifact
- validation or schema-backed check
- documented lossy mapping behavior

### Level 3

Expected evidence:
- privacy-policy or equivalent permission model
- policy-aware export, redaction path, or equivalent enforced behavior
- validation of the privacy surface where applicable

### Level 4

Expected evidence:
- benchmark artifacts or measurable run outputs
- trend/public-metrics path or equivalent repeatable reporting
- explicit evidence references and caveats

## Claim Format

Recommended format:

```text
Conformance: Level 3 (Privacy-Aware)
Source: markdown core/extended + privacy-policy.v1.json
Target: context.compact.json
Checks: validate_profile.py, validate_privacy_policy.py, validate_context_compact.py
Known loss: extended workflows omitted; source markdown remains canonical
Limits: no full round-trip restoration into canonical source files
```

Claims should be downgraded if one of the required evidence gates is missing.

## Current Repo Status

This repository aims to be:
- Level 4 for the maintained reference workflow;
- Level 2+ for external consumers using only interop artifacts.

Current repo justification:
- Level 2: interop export + validation + drift enforcement
- Level 3: machine-readable privacy policy + policy-aware compact/MCP exports
- Level 4: benchmark metrics, control deltas, evidence references, observed-behavior evidence layer

## Compatibility Rule

An integration should state the highest level it claims, the checks that justify it, and the fields or behaviors it does not preserve.
