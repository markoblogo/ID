# ID Spec v0.2

This is the current versioned entrypoint for the `ID` protocol surface.

`v0.2` does not replace the repo implementation with a fully separate spec corpus yet.
It tightens the boundary between:
- normative protocol commitments
- informative implementation, operations, and evidence docs

## What Changed From v0.1

- versioning semantics are now explicit and normative
- privacy/trust semantics have a clearer protocol boundary
- compatibility guidance is separated from observed behavior evidence
- the spec surface is easier to cite as a protocol contract rather than a repo tour

## Normative Documents For v0.2

- protocol scope and package model: `docs/PROTOCOL.md`
- versioning and update semantics: `docs/VERSIONING.md`
- lifecycle and operational contract: `docs/OPERATIONS.md`
- interop mapping contract: `docs/INTEROP_V1.md`
- evaluator scoring contract: `docs/EVALUATOR_PROTOCOL.md`
- conformance levels: `spec/CONFORMANCE.md`
- normative surface map: `spec/v0.2/NORMATIVE_SURFACE.md`

## Informative Documents For v0.2

- privacy and redaction guidance: `docs/PRIVACY.md`
- machine-readable privacy policy contract: `docs/PRIVACY_POLICY_V1.md`
- validation flow: `docs/VALIDATION.md`
- benchmark framework and public metrics: `docs/BENCHMARK.md`, `docs/MEASUREMENT.md`
- compatibility guidance: `docs/COMPATIBILITY.md`
- observed field evidence: `docs/OBSERVED_BEHAVIOR.md`
- compact target mapping: `docs/CONTEXT_JSON_MAPPING.md`
- hardening notes: `docs/HARDENING.md`
- minimal onboarding guide: `docs/MINIMAL_PROFILE.md`

## Current Interpretation Rule

If a conflict appears between:
- protocol commitments in the normative list
- implementation-facing guidance in informative docs

prefer the normative documents for protocol claims.

## Compatibility Note

`v0.2` should be treated as a maturity step, not a breaking redesign.

The repo still uses the same main artifacts:
- markdown source profiles
- `interop.v1.json`
- `context.compact.json`
- `mcp.context.resource.json`

What changes is the clarity of which documents define protocol obligations.
