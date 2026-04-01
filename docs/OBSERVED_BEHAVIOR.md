# Observed Behavior Notes

## Goal

Capture repo-tracked field evidence about how different AI tool families actually behave with `ID` artifacts.

This document is separate from `docs/COMPATIBILITY.md`:
- `COMPATIBILITY.md` describes intended mapping and expected loss boundaries
- this file records observed behavior, confidence, and evidence limits

Structured evidence notes live under:
- `evidence/observed-behavior/*.json`

Validation command:

```bash
python3 scripts/validate_observed_behavior.py
```

## Reading Rule

Each tool-family note should capture:
- observed onboarding mode
- observed best artifact
- observed degradation patterns
- confidence
- observation date
- relevant tool/model context when known

This is not vendor certification. It is repo-level operational evidence.

## Confidence Scale

- `high`: repeated direct repo use or benchmark-backed evidence
- `medium`: limited repeated use, partly benchmarked
- `low`: plausible operational observation, not yet broadly repeated

## ChatGPT Family

- observed onboarding mode:
  - best with compact explicit context plus handshake
  - long markdown source can work, but benefits from compression into L1/core or compact transport
- observed best artifact:
  - `context.compact.json`
  - for repo work, `profile.core.md` plus handshake is also effective
- observed degradation patterns:
  - freshness/trust semantics weaken if not stated explicitly
  - long-form profile nuance tends to compress into generalized behavior
  - project memory/instructions can drift from repo source of truth
- confidence:
  - `medium`
- observation date:
  - `2026-04-01`
- tool/model context:
  - repo-level usage patterns; not a vendor certification claim

## Claude Family

- observed onboarding mode:
  - strong with structured rules, heuristics, and selected extended-profile sections
  - best for strategic/protocol-heavy work when input remains bounded
- observed best artifact:
  - `context.compact.json` plus selected `profile.extended.md` excerpts
- observed degradation patterns:
  - compressed summaries can hide loss of provenance/changelog semantics
  - project knowledge can become convenience storage rather than audited source
- confidence:
  - `medium`
- observation date:
  - `2026-04-01`
- tool/model context:
  - informed by repo benchmark framing and repeated workflow assumptions

## Gemini Family

- observed onboarding mode:
  - shorter compact artifacts perform better than long prose-heavy profile dumps
  - explicit task framing matters more than broad narrative context
- observed best artifact:
  - `context.compact.json`
- observed degradation patterns:
  - longer prose can flatten unevenly
  - nuanced trust/provenance semantics often need direct restatement
- confidence:
  - `low`
- observation date:
  - `2026-04-01`
- tool/model context:
  - design-informed and repo-guided, not yet strongly field-tested here

## Copilot Family

- observed onboarding mode:
  - best when `ID` is used as repo-local markdown plus explicit coding constraints
  - personal context outside immediate code work is weaker unless surfaced manually
- observed best artifact:
  - `profile.core.md`
  - repo instructions plus local task context
- observed degradation patterns:
  - portability drops outside repository boundaries
  - non-code preferences are more likely to be ignored or underused
- confidence:
  - `medium`
- observation date:
  - `2026-04-01`
- tool/model context:
  - assumes repo-native coding assistant behavior, not generalized long-memory usage

## Local Agents / Custom Orchestrators

- observed onboarding mode:
  - highest fidelity when markdown stays canonical and machine artifacts are transport-specific views
  - best results come from explicit validation, drift-checks, and policy-aware exports
- observed best artifact:
  - `interop.v1.json`
  - `context.compact.json`
  - `mcp.context.resource.json`
- observed degradation patterns:
  - prose nuance still flattens in machine artifacts
  - poor orchestration hygiene can hide adapter-specific behavior behind structured transport
- confidence:
  - `high`
- observation date:
  - `2026-04-01`
- tool/model context:
  - directly supported by repo scripts, validators, and generated artifacts

## Current Evidence Limits

- vendor-family notes remain repo-level observations, not broad external studies
- some controls remain synthetic matched controls rather than independent live runs
- non-local vendor behavior should be treated as provisional until expanded by repeated task evidence

## Update Rule

Update this document when:
- repeated real use changes the recommended onboarding mode for a tool family
- a benchmark/control pattern materially changes expected behavior
- a new artifact becomes the clearly preferred transport for a tool family
- observed degradation differs from intended mapping in a stable way
