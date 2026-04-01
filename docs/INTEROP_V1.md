# Interop v1 Specification and Migration

## 1. Purpose

Define stable field naming for cross-tool interoperability and migration from current markdown-first profile format.

## 2. v1 Envelope

```json
{
  "interop_version": "1.0.0",
  "owner_id": "markoblogo",
  "generated_at": "2026-04-01",
  "profiles": {
    "core": {"...": "..."},
    "extended": {"...": "..."}
  }
}
```

## 3. Core Profile v1 Fields

- `metadata.profile_id`
- `metadata.owner_alias`
- `metadata.version`
- `metadata.created_at`
- `metadata.updated_at`
- `metadata.freshness_ttl_days` (integer)
- `metadata.trust_level`
- `communication`
- `rules`
- `quality_bar`
- `priority_domains`
- `tool_notes`

## 4. Migration From v0 Markdown

Current v0 source:
- `profiles/<owner>/profile.core.md`
- `profiles/<owner>/profile.extended.md`

Migration steps:
1. parse front matter into `metadata` block.
2. map markdown sections into structured arrays/objects.
3. map `## Domain Workflows` by `###` subsections.
4. keep unknown sections under `extensions`.
5. validate output against `schemas/interop-v1.schema.json`.

## 5. Compatibility Rules

- v1 consumers must ignore unknown fields in `extensions`.
- producers must preserve semantically equivalent data when round-tripping.
- date fields must stay in `YYYY-MM-DD`.
- broader target compatibility and loss boundaries are tracked in `docs/COMPATIBILITY.md`.

## 6. Artifact Policy (`interop.v1.json`)

- source of truth remains markdown profiles (`profile.core.md`, `profile.extended.md`).
- `profiles/<owner>/interop.v1.json` is a versioned interoperability artifact and should be committed.
- when profile markdown changes, regenerate and commit `interop.v1.json` in the same change set.

## 7. Migration Helper Script

Use:

```bash
python3 scripts/export_interop_v1.py --owner-id markoblogo
```

Validate:

```bash
python3 scripts/validate_interop_v1.py --owner-id markoblogo
```

Output:
- `profiles/<owner>/interop.v1.json`

## 8. Non-Goals

- v1 does not replace markdown source of truth.
- v1 does not include raw transcript archives.
