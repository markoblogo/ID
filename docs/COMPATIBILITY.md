# Compatibility Matrix and Mapping Rules

## 1. Purpose

`ID` should act as a bridge to existing AI workflows and ecosystems, not as an isolated format.

This document defines:
- target integration classes;
- current compatibility expectations;
- mapping rules;
- known loss boundaries.

It distinguishes:
- **intended mapping**: what an exporter/adapter is designed to preserve
- **observed behavior**: what this repo currently implements and validates

Observed field notes live in:
- `docs/OBSERVED_BEHAVIOR.md`

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

## 5. Concrete Tool Matrix

| Tool / environment | Best source input path | Best target artifact | What maps well | What degrades | What is lost | Recommended operating mode |
|---|---|---|---|---|---|---|
| ChatGPT | `profile.core.md` + handshake; optionally `profile.extended.md` for longer tasks | `context.compact.json` or carefully compressed project instructions | communication style, quality bar, explicit rules, short tool notes | freshness/trust semantics become passive unless surfaced explicitly in prompt text | changelog discipline, full provenance, richer workflow nuance | use L1/core by default; add handshake and explicit uncertainty/freshness note |
| Claude | `profile.core.md` + selected `profile.extended.md` sections | `context.compact.json` or project knowledge/instructions | constraints, structured reasoning preferences, domain heuristics, review style | policy/freshness semantics are preserved only if written into instruction layer | round-trip fidelity, changelog continuity, full extensions | use compact export plus 1-2 targeted extended sections for strategic work |
| Gemini | `profile.core.md` first; compact export for portability | `context.compact.json` | concise rules, quality bar, task framing, high-level domains | long structured profile prose may compress unevenly | detailed provenance/history, nuanced layered trust semantics | prefer compact export over long prose; keep explicit loss notes when sharing |
| Copilot / repo-native coding assistants | `profile.core.md` + repo instructions + local task context | markdown source profile plus compact export for wrappers | coding constraints, brevity/style expectations, safety rules, repo workflow alignment | non-repo personal context is weaker unless surfaced manually | cross-tool memory continuity, rich personal glossary beyond repo task | use markdown source in repo, compact export only for bridging or automation |
| Local agents / custom orchestrators | markdown source + `interop.v1.json` + `privacy-policy.v1.json` | `interop.v1.json`, `context.compact.json`, or `mcp.context.resource.json` depending transport | most structured fields, freshness, trust, policy-aware export behavior | prose nuance still flattens in machine artifacts | zero-loss round-trip from markdown source | prefer markdown as source of truth, machine artifacts as transport-specific views |

Notes:
- `ChatGPT`, `Claude`, and `Gemini` rows describe tool families, not vendor-guaranteed product contracts.
- `Copilot` row assumes repo-centric coding workflows rather than general long-memory chat use.
- `Local agents` is the highest-fidelity path because the surrounding orchestration can honor explicit artifacts directly.

## 6. Mapping Rules

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

## 7. Vendor-Specific Guidance

### ChatGPT family

Best fit:
- compact, explicit, bounded context blocks
- short operational constraints
- handshake-led onboarding

Watch for:
- project memory or instructions being treated as sufficient replacement for freshness/trust metadata
- silent drift when the profile is updated outside the tool

### Claude family

Best fit:
- structured rules and heuristics
- deeper profile sections for long-form reasoning or protocol work

Watch for:
- good reasoning over compressed summaries that may still hide lossy flattening
- project knowledge acting as convenience storage rather than auditable source of truth

### Gemini family

Best fit:
- shorter compact artifacts
- explicit task framing and bounded constraints

Watch for:
- uneven handling of longer prose-heavy source profiles
- weaker preservation of nuanced provenance unless restated directly

### Copilot family

Best fit:
- repo-local markdown profile plus repo instructions
- clear coding constraints and review preferences

Watch for:
- reduced portability outside the repository boundary
- weaker support for personal context unrelated to immediate code work

### Local agents / orchestrators

Best fit:
- direct consumption of generated machine artifacts
- policy-aware exports and MCP transport

Watch for:
- assuming generated transport artifacts are complete replacements for markdown source
- hidden adapter behavior if custom orchestration layers are not documented

## 8. Non-Negotiable Semantics

The following should never be silently dropped without documentation:
- `updated_at`
- `freshness_ttl_days`
- trust level
- explicit `never do` rules
- ask-before constraints
- uncertainty / confidence semantics when benchmark results are exported

If a target cannot preserve these directly, note the degradation explicitly.

## 9. Compatibility Claims

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

## 10. Next Adapters

Recommended next compatibility work:
- expand import behavior beyond lossy markdown draft generation
- add stronger round-trip / drift checks for compact target consumers
- extend round-trip loss tests for future exporters and importers
- document observed behavior, not just intended mapping, for major vendor tools

Reference MCP-oriented wrapper example:
- `integrations/mcp/context.resource.example.json`

## 11. Intended vs Observed Behavior

### Intended mapping

The protocol intent is:
- markdown source remains canonical
- machine artifacts are transport or portability views
- lossy mappings must be documented, not hidden

### Observed behavior in this repo today

Currently implemented and validated:
- markdown -> `interop.v1.json`
- markdown -> `context.compact.json`
- markdown -> `mcp.context.resource.json`
- `context.compact.json` -> markdown draft import
- `mcp.context.resource.json` -> markdown draft import

Currently documented but not fully observed/certified across vendors:
- ChatGPT family behavior
- Claude family behavior
- Gemini family behavior
- Copilot family behavior

Reference observed-notes layer:
- `docs/OBSERVED_BEHAVIOR.md`

Not yet implemented:
- true round-trip restoration into canonical source profiles
- import adapters that preserve full provenance/history
- vendor-specific behavioral certification beyond repo-level guidance

## 12. Non-Goals

- `ID` does not try to replace MCP.
- `ID` does not assume one chat vendor's memory model is portable.
- `ID` does not claim zero-loss export across all targets.
