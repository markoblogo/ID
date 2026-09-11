# agents.md Integration

## Contract

Before substantive task execution:

1. Run `pre_task` hook.
2. Load the returned `primary_human_bootstrap` file and only the relevant files from `preferred_human_bootstrap`.
3. Apply relevant owner constraints without repeating them.
4. Execute the task, asking only when a material uncertainty blocks progress.
5. Run `post_task` after meaningful use or change.

## Hook Commands

```bash
scripts/run_integration_hook.sh pre_task --owner-id markoblogo --target agentsmd
```

The hook prints machine-readable bootstrap pointers. Consumers should use those pointers instead of hardcoding a profile filename.

```bash
scripts/run_integration_hook.sh post_task \
  --owner-id markoblogo \
  --session-context "agents.md coding session" \
  --sections-used "profile.core.md, handshake.md" \
  --changes-made "Updated integration flow" \
  --open-questions "None"
```
