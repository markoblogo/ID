# agents.md Integration

## Contract

Before substantive task execution:

1. Run `pre_task` hook.
2. Load `profiles/<owner>/profile.core.md`.
3. Load `profiles/<owner>/handshake.md`.
4. Confirm understanding in 5-10 bullets.
5. Execute task.
6. Run `post_task` hook.

## Hook Commands

```bash
scripts/run_integration_hook.sh pre_task --owner-id markoblogo --target agentsmd
```

```bash
scripts/run_integration_hook.sh post_task \
  --owner-id markoblogo \
  --session-context "agents.md coding session" \
  --sections-used "profile.core.md, handshake.md" \
  --changes-made "Updated integration flow" \
  --open-questions "None"
```
