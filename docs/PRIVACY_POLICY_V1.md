# Machine-Readable Privacy Policy v1

## Goal

`privacy-policy.v1.json` is the machine-readable companion to `docs/PRIVACY.md`.

It defines which profile or data paths are:
- `always_share`
- `local_only`
- `task_class_scoped`

This layer is intended to make trust/privacy behavior enforceable by tooling, not only described in prose.

## Artifact

Per-owner policy artifact:

- `profiles/<owner>/privacy-policy.v1.json`

Validation command:

```bash
python3 scripts/validate_privacy_policy.py --owner-id <owner>
```

## Core Fields

- `policy_version`: semver for the policy contract
- `owner_id`: profile owner id
- `updated_at`: last meaningful policy update date
- `default_access`: fallback access rule when no path-specific rule exists
- `task_classes`: allowed task-class vocabulary for scoped sharing
- `rules`: field/path-specific access rules

## Access Levels

### `always_share`

Use for low-risk operational context that should travel with the profile by default.

Examples:
- communication style
- core safety constraints
- priority domains

### `local_only`

Use for content that should never leave the local/private boundary by default.

Examples:
- local environment details
- normalized private source material
- unredacted archives

### `task_class_scoped`

Use when data is shareable only for a relevant task family.

Examples:
- domain workflows for coding/research/writing
- specialized image/video preferences

## Rule Shape

Each rule defines:
- `field_path`
- `access`
- `rationale`
- `allowed_task_classes` when `access=task_class_scoped`

## Current Scope

This v1 policy layer is validation-first.

It does not yet automatically gate exporters. That is the next integration step.
