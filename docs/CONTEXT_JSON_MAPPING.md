# Compact Context Mapping

## 1. Purpose

Define a compact portable export target for systems that want a small, structured context payload rather than the full markdown or `interop.v1.json` surface.

This target is intended for:
- project instructions
- prompt bundle files
- lightweight context loaders
- wrappers that need a short, explicit payload

This is a compatibility target, not the canonical source of truth.

## 2. Source and Target

Source:
- `profiles/<owner>/profile.core.md`
- optionally selected data from `profile.extended.md`

Target:
- `context.compact.json`
- schema: `schemas/context-compact-v0.schema.json`
- starter template: `templates/context.compact.json`

## 3. Design Goal

Preserve the highest-value portable fields with minimal size:
- who this profile is for
- freshness and trust metadata
- communication style
- explicit task rules
- quality bar
- priority domains
- compact tool notes

## 4. Target Shape

```json
{
  "context_version": "0.1.0",
  "owner_id": "markoblogo",
  "updated_at": "2026-04-01",
  "freshness_ttl_days": 14,
  "trust_level": "trusted",
  "communication": [],
  "rules": {
    "always_do": [],
    "never_do": [],
    "ask_before": [],
    "default_assumptions": []
  },
  "quality_bar": [],
  "priority_domains": [],
  "tool_notes": [],
  "loss_notes": []
}
```

## 5. Mapping Rules

### Metadata

- `owner_id` <- `metadata.owner_alias` or profile owner directory name
- `updated_at` <- `metadata.updated_at`
- `freshness_ttl_days` <- `metadata.freshness_ttl_days`
- `trust_level` <- `metadata.trust_level`

### Communication

Map `## Communication Style` bullets or equivalent typed values into:
- `communication[]`

Compression rule:
- preserve intent, not heading prose;
- split long multi-part statements only if needed for clarity.

### Rules

Map `Task Execution Rules` into:
- `rules.always_do`
- `rules.never_do`
- `rules.ask_before`
- `rules.default_assumptions`

This block is non-negotiable. Do not flatten all rules into one list.

### Quality / Domains / Tool Notes

Map:
- `Quality Bar` -> `quality_bar[]`
- `Priority Domains` -> `priority_domains[]`
- `Tool-Specific Notes` -> `tool_notes[]`

## 6. Loss Rules

Fields intentionally omitted from the compact target:
- long corrections history
- extended workflows
- lexicon
- long environment assumptions
- detailed provenance
- benchmark evidence fields

These omissions must be declared in `loss_notes`.

Recommended default `loss_notes`:
- `"Extended workflows omitted"`
- `"Historical corrections omitted"`
- `"Use full profile or interop.v1.json for richer context"`

## 7. When to Use This Target

Use `context.compact.json` when:
- the destination accepts only a short structured payload;
- startup latency matters more than richness;
- you need a portable summary for a new tool;
- L1/core semantics are enough for the task.

Do not use it as the only artifact when:
- provenance matters;
- privacy classes differ by task;
- detailed workflows and repeated misalignments are operationally important;
- round-trip fidelity is required.

## 8. Compatibility Claim

The compact target should be described as:
- source-preserving for core rules and style
- intentionally lossy for extended and historical layers

Suggested claim:

```text
Conformance: Level 2 (Portable)
Target: context.compact.json
Loss profile: medium
Preserves: communication, explicit rules, quality bar, domains, tool notes
Omits: extended workflows, history, provenance-heavy context
```

## 9. Next Step

Future implementation may add:
- exporter script for `context.compact.json`
- round-trip tests
- target-specific emitters for known `context.json`-style consumers
