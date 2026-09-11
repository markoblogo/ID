# Privacy and redaction

ID is private-first. Keep canonical profiles and raw source material outside public repositories unless they were deliberately prepared for publication.

## Data classes

- Direct identifiers: legal names, email, phone, addresses, government identifiers, account handles.
- Sensitive context: health, family, finances, private conversations, detailed location and infrastructure.
- Operational preferences: communication style, workflow constraints, quality criteria, and tool habits.

Low-risk fields can become identifying in combination. Review every export for its actual recipient and purpose.

## Policy model

Each owner directory uses `privacy-policy.v1.json`. The current format defines:

- `default_access`: the fallback for unlisted fields; generated starters use `local_only`;
- `task_classes`: allowed workflow scopes;
- `rules`: field paths with `always_share`, `local_only`, or `task_class_scoped` access;
- `allowed_task_classes`: required for scoped rules.

Validate it with:

```sh
idctl validate-privacy --owner-id <owner-id>
```

Compact and MCP resource exports fail when the policy is missing or invalid. A supported legacy list policy is normalized only in memory; ID preserves the original file and keeps unlisted fields local-only.

## Before sharing

1. Confirm the owner and task class.
2. Validate the profile and privacy policy.
3. Generate a new compact or MCP resource export.
4. Search the output for direct identifiers and sensitive combinations.
5. Share only the reviewed generated artifact.

Generating a file does not upload it. The receiving tool's retention, training, and access policies remain outside ID's control.

If sensitive data is published, stop distribution, rotate exposed credentials, remove the data from the current branch, assess whether history rewrite is needed, and record the response without repeating the sensitive material.
