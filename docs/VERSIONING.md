# Versioning and Update Semantics

## Goal

Define what counts as a meaningful profile change, when versions should bump, and when freshness metadata must be updated.

This document is normative for `ID Spec v0.1`.

## 1. Source of Truth

Canonical source of truth:
- `profiles/<owner>/profile.core.md`
- `profiles/<owner>/profile.extended.md`
- other markdown source files explicitly treated as profile authority

Generated artifacts such as:
- `interop.v1.json`
- `context.compact.json`
- `mcp.context.resource.json`

must be regenerated from source, but they do not define canonical version meaning by themselves.

## 2. Meaningful Diff Semantics

A change is **meaningful** if it affects how an agent should behave, what it should assume, or how trust/freshness should be interpreted.

Meaningful changes include:
- adding or removing stable preferences
- changing constraints or safety boundaries
- changing quality bar or definition of done
- changing priority domains or decision heuristics
- changing trust level semantics for active profile content
- adding new recurring workflows or known misalignments
- changing privacy-policy rules that affect export behavior

Usually **not** meaningful by themselves:
- typo fixes that do not change meaning
- formatting-only edits
- reordering bullets without semantic change
- regenerating derived artifacts from unchanged source meaning

Borderline rule:
- if an agent would behave differently after the edit, treat it as meaningful

## 3. Version Bump Policy

Profile versions use semver-style `MAJOR.MINOR.PATCH`.

### PATCH

Bump PATCH when:
- wording is clarified without changing intended behavior
- small corrections improve precision
- examples or phrasing are refined with no material change in rules

### MINOR

Bump MINOR when:
- new stable preferences or workflows are added
- a section materially changes agent behavior or expected output style
- new recurring constraints, misalignments, or heuristics are added
- machine-readable policy changes alter allowed export scope

### MAJOR

Bump MAJOR when:
- profile structure changes in a backward-breaking way
- protocol-level assumptions change so old integrations or prompts should not rely on previous interpretation
- semantics are removed or inverted in a way that breaks compatibility

## 4. Freshness / Update Policy

`updated_at` should change whenever the profile meaning changes in a meaningful way.

Update `updated_at` when:
- version is bumped
- stable preferences or constraints change
- new behavioral evidence is promoted into the canonical profile
- privacy policy changes alter exportable scope

You may keep `updated_at` unchanged for:
- formatting-only edits
- typo fixes with no semantic effect
- regeneration of derived JSON artifacts

`freshness_ttl_days` is not a version number. It is an operational confidence horizon.

Guidance:
- shorter TTL for fast-changing or still-calibrating profiles
- longer TTL for well-established profiles with stable habits

## 5. Changelog Expectation

When a meaningful change happens:
1. update the relevant source profile
2. bump the profile version appropriately
3. update `updated_at`
4. regenerate derived artifacts
5. record the reason in changelog/session history when applicable

## 6. Derived Artifact Policy

Generated artifacts should track source meaning, not invent new version semantics.

Rules:
- regenerate after meaningful source changes
- do not bump source version only because a derived file was regenerated
- if a derived artifact changes because exporter logic changed, document that separately from profile semantic changes

## 7. Enforcement Guidance

Current enforcement posture:
- structural freshness checks: `scripts/validate_profile.py`
- quality heuristics: `scripts/lint_profile_quality.py`
- artifact drift: `make drift-check`

Human judgment is still required for:
- deciding whether a diff is semantic or cosmetic
- choosing PATCH vs MINOR in borderline cases
- deciding when a policy change is backward-breaking enough to justify MAJOR

## 8. Default Rule

If unsure:
- prefer bumping version rather than silently changing behavior
- prefer updating `updated_at` rather than overstating freshness
- prefer documenting semantic uncertainty explicitly in changelog or confidence notes
