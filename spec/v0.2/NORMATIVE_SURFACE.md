# Normative Surface Map

## Goal

State which documents define protocol obligations for `ID Spec v0.2`, and which documents are informative support material only.

## Normative

These documents define protocol-facing commitments and may be cited for compatibility or conformance claims:

- `docs/PROTOCOL.md`
  - package levels
  - mandatory metadata
  - handshake contract
  - trust levels
  - source-of-truth rule
- `docs/VERSIONING.md`
  - meaningful diff semantics
  - version bump policy
  - freshness/update policy
  - derived artifact policy
- `docs/OPERATIONS.md`
  - lifecycle expectations for maintaining the protocol in practice
- `docs/INTEROP_V1.md`
  - structured export contract for `interop.v1.json`
- `docs/EVALUATOR_PROTOCOL.md`
  - evaluator/rubric contract for benchmark interpretation
- `spec/CONFORMANCE.md`
  - conformance level definitions

## Informative

These documents guide implementation, operations, evidence, or adoption, but do not define the protocol by themselves:

- `docs/PRIVACY.md`
- `docs/PRIVACY_POLICY_V1.md`
- `docs/VALIDATION.md`
- `docs/BENCHMARK.md`
- `docs/MEASUREMENT.md`
- `docs/COMPATIBILITY.md`
- `docs/OBSERVED_BEHAVIOR.md`
- `docs/CONTEXT_JSON_MAPPING.md`
- `docs/HARDENING.md`
- `docs/MINIMAL_PROFILE.md`

## Claim Rule

When making a protocol or compatibility claim:
1. cite the relevant normative document
2. cite any informative document only as supporting context
3. do not treat observed repo behavior as a substitute for normative contract text

## Default Rule

If a document is ambiguous:
- protocol obligation claims should resolve toward the normative set
- operational examples and tool guidance should resolve toward the informative set
