# Interop v1 Specification and Migration

## 1. Purpose

Define stable field naming for cross-tool interoperability and migration from current markdown-first profile format.

## 2. v1 Envelope

```json
{
  "interop_version": "1.0.0",
  "owner_id": "markoblogo",
  "generated_at": "2026-03-31",
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
- `metadata.freshness_ttl_days`
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
3. keep unknown sections under `extensions`.
4. validate output against `schemas/interop-v1.schema.json`.

## 5. Compatibility Rules

- v1 consumers must ignore unknown fields.
- producers must preserve semantically equivalent data when round-tripping.
- date fields must stay in `YYYY-MM-DD`.

## 6. Migration Helper Script

Use:

```bash
python3 scripts/export_interop_v1.py --owner-id markoblogo
```

Output:
- `profiles/<owner>/interop.v1.json`

## 7. Non-Goals

- v1 does not replace markdown source of truth yet.
- v1 does not include raw transcript archives.
