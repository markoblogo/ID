# Contributing to ID Protocol

## Change Types

- `spec`: protocol semantics changed.
- `template`: authoring templates changed.
- `ops`: operational flow changed.
- `schema`: machine-readable validation changed.
- `rfc`: proposal for future protocol or compatibility changes.

## Pull Request Checklist

- update version where applicable;
- document migration impact;
- add changelog note;
- avoid breaking template field names without migration section.
- use `spec/RFC/README.md` when changing protocol semantics or compatibility expectations.

## Compatibility Promise (v0.x)

Until `v1.0.0`, breaking changes are allowed but must be marked clearly in PR title: `[breaking]`.

## Spec Surface

- versioned spec entrypoint: `spec/v0.1/README.md`
- conformance levels: `spec/CONFORMANCE.md`
- spec changelog: `spec/CHANGELOG.md`
