# Threat Model

## Goal

Define the main trust and failure boundaries for `ID` as a portable human-AI context protocol.

This document is not a security audit. It is an operational threat model for profile quality, privacy, interoperability, and benchmark interpretation.

## System Boundary

The `ID` trust surface includes:
- markdown source profiles under `profiles/<owner>/`
- generated artifacts such as `interop.v1.json`, `context.compact.json`, and `mcp.context.resource.json`
- machine-readable privacy policy in `privacy-policy.v1.json`
- benchmark runs and public metrics artifacts
- redaction and export scripts

Out of scope:
- vendor-side retention and training policies of external AI providers
- endpoint compromise on a user's machine
- transport encryption beyond the chosen tool or platform

## Threat Classes

### 1. Stale Profile Risk

Failure mode:
- source profiles stop reflecting the user's current preferences, constraints, or workflows

Impact:
- agents optimize for outdated behavior
- benchmark outcomes become less meaningful
- incorrect guidance propagates across tools through valid but stale exports

Mitigations:
- `updated_at` and `freshness_ttl_days` in profile front matter
- `scripts/validate_profile.py`
- `profile_freshness` in public metrics
- changelog/update workflow

Residual risk:
- stale-but-plausible profiles can still pass basic structure checks
- quality depends on actual maintenance discipline, not just timestamps

### 2. Oversharing / Privacy Leakage

Failure mode:
- sensitive personal context is exported or shared beyond intended scope

Impact:
- privacy breach
- irreversible disclosure if committed or sent to third-party systems
- trust loss in the protocol itself

Mitigations:
- `docs/PRIVACY.md`
- `docs/PRIVACY_POLICY_V1.md`
- `profiles/<owner>/privacy-policy.v1.json`
- policy-aware compact and MCP exports
- redaction tooling and publish guard

Residual risk:
- policy may be incomplete or too permissive
- safe low-risk fields can become sensitive in aggregate

### 3. Policy Drift Risk

Failure mode:
- machine-readable policy no longer matches actual intent or source profile semantics

Impact:
- exporters produce technically valid but normatively wrong outputs
- operators assume a stronger privacy posture than actually enforced

Mitigations:
- dedicated privacy policy schema and validator
- `make privacy-policy`
- `make validate` now checks policy before exports

Residual risk:
- semantic drift is still possible if policy remains syntactically valid
- no policy intent linter yet

### 4. Partial / Lossy Export Risk

Failure mode:
- downstream formats preserve only part of the source profile and users overestimate fidelity

Impact:
- silent context loss across tools
- wrong expectations about what a target artifact can represent
- degraded decisions made from compact or MCP transport layers

Mitigations:
- explicit source-of-truth rule: markdown profile files remain canonical
- compatibility docs and loss notes
- separate artifacts for interop, compact, and MCP transport
- drift-check on generated artifacts

Residual risk:
- users may still treat exported artifacts as full round-trip representations
- import adapters and round-trip loss tests are not implemented yet

### 5. Benchmark Misread Risk

Failure mode:
- public metrics are overclaimed as universal proof rather than bounded repo-level evidence

Impact:
- false confidence in portability or quality gains
- invalid product claims
- poor decisions based on synthetic or narrow benchmark coverage

Mitigations:
- evaluator protocol
- explicit metric definitions
- documented control runs and comparison groups
- tokenizer-aware metrics kept opt-in and non-canonical

Residual risk:
- current controls are still limited and partly synthetic
- repo-native proof is not the same as broad external validation

### 6. Synthetic Control Misuse

Failure mode:
- matched `no_id` controls are treated as if they were live independent benchmark runs

Impact:
- inflated claims about causal improvement
- underestimation of real-world tool variance

Mitigations:
- explicit documentation that current control runs are synthetic matched controls
- separation between canonical tracked metrics and optional local instrumentation

Residual risk:
- readers may still overlook the distinction unless surfaced prominently in summaries

### 7. Weak Profile Quality Risk

Failure mode:
- canonical source profiles are vague, contradictory, or underspecified

Impact:
- all downstream exports remain formally valid but operationally weak
- benchmarks measure low-quality source context rather than protocol strength

Mitigations:
- `scripts/lint_profile_quality.py`
- advisory `make lint-profile`
- benchmark evaluator protocol

Residual risk:
- linter is heuristic and currently advisory-only
- no provenance-quality scoring yet

## Trust Posture

The current protocol posture is:
- source-first
- private-first
- export-with-loss-notes
- benchmark-with-explicit-caveats

This means `ID` should be treated as:
- a controlled context protocol with explicit boundaries,
- not as a guarantee that every export is complete,
- and not as proof that every benchmark delta generalizes across vendors or tasks.

## Next Hardening Steps

Priority order:
1. decide whether profile-quality linting should remain advisory or become strict in canonical validation
2. define version bump and diff semantics
3. add tool/vendor compatibility matrix
4. add import adapters and round-trip loss tests
