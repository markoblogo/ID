# Compatibility Matrix and Mapping Rules

## 1. Purpose

`ID` should act as a bridge to existing AI workflows and ecosystems, not as an isolated format.

This document defines:
- target integration classes;
- current compatibility expectations;
- mapping rules;
- known loss boundaries.

## 2. Canonical Source of Truth

Canonical source:
- `profiles/<owner>/profile.core.md`
- `profiles/<owner>/profile.extended.md`

Portable machine artifact:
- `profiles/<owner>/interop.v1.json`

Rule:
- markdown profiles remain source of truth;
- exported compatibility artifacts must document any lossy mapping behavior;
- consumers should prefer explicit preservation over silent flattening.

## 3. Target Classes

### A. Chat-Native Memory Systems

Examples:
- ChatGPT memory / project instructions
- Claude project knowledge / project instructions
- Gemini saved context / workspace instructions

Typical strengths:
- easy onboarding inside one product
- good low-friction reuse

Typical limitations:
- context is product-local
- freshness and changelog discipline are usually implicit
- export / auditability is weak

### B. Prompt / Context File Conventions

Examples:
- repo instructions
- `context.json`-like formats
- portable markdown profile files

Typical strengths:
- explicit and versionable
- easy to review in git

Typical limitations:
- semantics vary widely
- no guaranteed privacy or benchmark model

### C. Tool / Data Access Protocols

Examples:
- MCP-style tool and data access wrappers

Typical strengths:
- transport for structured context and tools
- clear system boundaries

Typical limitations:
- transport layer does not define user preference semantics by itself
- profile portability still requires a stable content model

## 4. Initial Compatibility Matrix

| Target | Current status | Suggested conformance | Main preserved data | Known loss / risk |
|---|---|---:|---|---|
| Markdown-native repo workflows | strong | 4 | nearly all profile structure | low, if docs are kept in sync |
| `interop.v1.json` consumers | strong | 2-4 | metadata, rules, communication, workflows, extensions | markdown nuance may flatten into arrays/objects |
| ChatGPT / Claude / Gemini project instructions | partial | 1-2 | core constraints, style, quality bar, short tool notes | freshness, changelog, trust semantics usually become manual |
| MCP-based wrappers | partial | 2-4 | structured payload transport, explicit handoff | MCP is transport, not semantic profile standard |
| `context.json`-like prompt bundles | partial | 2 | compact portable profile blocks | field naming and round-trip semantics vary by implementation |

## 5. Mapping Rules

### Markdown -> `interop.v1.json`

Current status:
- implemented and validated in this repo

Mapping principles:
- front matter -> `metadata`
- stable known sections -> typed fields
- unknown sections -> `extensions`
- date fields stay `YYYY-MM-DD`

Loss profile:
- medium-low
- heading nuance and prose structure may flatten into bullet arrays

### Markdown -> chat/project instructions

Recommended mapping:
- use L1/core profile only by default
- include handshake instructions
- compress to explicit rules, style, and quality bar

Loss profile:
- medium-high
- changelog discipline, trust level, freshness, and provenance often become manual

### Markdown / Interop -> MCP wrapper payload

Recommended mapping:
- pass profile payload as structured resource data
- keep trust/freshness fields explicit
- expose tool-specific policy in wrapper metadata, not hidden prose

Loss profile:
- low to medium
- depends on wrapper discipline rather than protocol limitations

### Markdown -> context.json-like bundles

Recommended mapping:
- export a compact block for communication style, rules, domains, and tool notes
- preserve full profile externally when round-trip fidelity matters

Reference target:
- `docs/CONTEXT_JSON_MAPPING.md`
- `schemas/context-compact-v0.schema.json`
- `templates/context.compact.json`

Loss profile:
- medium
- target-specific field semantics differ and may not preserve all sections cleanly

## 6. Non-Negotiable Semantics

The following should never be silently dropped without documentation:
- `updated_at`
- `freshness_ttl_days`
- trust level
- explicit `never do` rules
- ask-before constraints
- uncertainty / confidence semantics when benchmark results are exported

If a target cannot preserve these directly, note the degradation explicitly.

## 7. Compatibility Claims

Any integration or exporter should state:
- claimed conformance level from `spec/CONFORMANCE.md`
- source format used
- target format used
- known lossy fields or behaviors

Recommended claim format:

```text
Conformance: Level 2 (Portable)
Source: markdown core/extended + interop.v1.json
Target: project instructions
Known loss: freshness and trust semantics preserved as comments, not enforced fields
```

## 8. Next Adapters

Recommended next compatibility work:
- add round-trip / drift checks for compact target consumers
- round-trip loss tests for future exporters

Reference MCP-oriented wrapper example:
- `integrations/mcp/context.resource.example.json`

## 9. Non-Goals

- `ID` does not try to replace MCP.
- `ID` does not assume one chat vendor's memory model is portable.
- `ID` does not claim zero-loss export across all targets.
