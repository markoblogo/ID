# Contributing to ID Protocol

## Change Types

- `spec`: protocol semantics changed.
- `template`: authoring templates changed.
- `ops`: operational flow changed.
- `schema`: machine-readable validation changed.

## Pull Request Checklist

- update version where applicable;
- document migration impact;
- add changelog note;
- avoid breaking template field names without migration section.

## Compatibility Promise (v0.x)

Until `v1.0.0`, breaking changes are allowed but must be marked clearly in PR title: `[breaking]`.
