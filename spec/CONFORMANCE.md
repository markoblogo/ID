# Conformance Model

`ID` implementations do not all need to support the same surface area.

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

### Level 2: Portable

Includes Level 1, plus:
- export or consume `interop.v1.json`;
- preserve unknown fields or extensions safely;
- document any lossy mapping behavior.

### Level 3: Privacy-Aware

Includes Level 2, plus:
- support redaction or permission-aware sharing;
- distinguish local-only vs shareable context where possible;
- expose privacy limitations clearly.

### Level 4: Measurable

Includes Level 3, plus:
- support benchmark task execution or benchmark result consumption;
- preserve evidence references;
- emit data suitable for trend comparison.

## Current Repo Status

This repository aims to be:
- Level 4 for the maintained reference workflow;
- Level 2+ for external consumers using only interop artifacts.

## Compatibility Rule

An integration should state the highest level it claims and the fields or behaviors it does not preserve.
