# Context Compact Mapping

## Goal

`context.compact.json` is a portable, loss-aware target for short onboarding and tool handoff.

It is intentionally smaller than the full `interop.v1.json` artifact and is designed for contexts where a compact, operationally useful profile is preferable to a richer protocol package.

## Source of Truth

Canonical source remains the markdown profile set plus the generated `interop.v1.json` artifact.

`context.compact.json` is a derived export target, not the source of truth.

## Output Contract

Fields preserved in the compact target:
- `context_version`
- `owner_id`
- `updated_at`
- `freshness_ttl_days`
- `trust_level`
- `communication`
- `rules.always_do`
- `rules.never_do`
- `rules.ask_before`
- `rules.default_assumptions`
- `quality_bar`
- `priority_domains`
- `tool_notes`
- `loss_notes`

## Loss Profile

The compact target omits or compresses:
- extended workflows
- historical corrections
- most rich per-domain detail
- provenance/context depth that belongs in full interop or source markdown

## Privacy-Policy Behavior

`export_context_compact.py` now applies `privacy-policy.v1.json` when it exists.

Default behavior:
- `always_share` fields remain in the export
- `local_only` fields are stripped
- `task_class_scoped` fields are included only when `--task-class <name>` is provided and allowed by policy

If fields are omitted by policy, the exporter records that in `loss_notes` rather than silently leaking or silently dropping context.

Example generic export:

```bash
python3 scripts/export_context_compact.py --owner-id <owner-id>
```

Example task-scoped export:

```bash
python3 scripts/export_context_compact.py --owner-id <owner-id> --task-class coding
```

## Notes

The compact target remains intentionally conservative.

Use `interop.v1.json` when you need richer context, and keep the markdown profile files as the canonical editable source.
