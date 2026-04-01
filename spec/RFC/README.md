# RFC Process

Use RFCs for changes that alter protocol semantics, interoperability, or compatibility expectations.

## When an RFC is required

Open an RFC for:
- breaking spec changes;
- new mandatory fields;
- new conformance levels;
- interop mapping changes with round-trip impact;
- privacy model changes that affect sharing behavior.

## Lightweight RFC format

Recommended file name:
- `spec/RFC/0001-short-name.md`

Recommended sections:
- Summary
- Motivation
- Proposed change
- Compatibility impact
- Migration plan
- Open questions

## Review rule

Do not merge significant protocol changes until:
- the RFC exists;
- compatibility impact is documented;
- related docs or schemas are updated in the same change set.
