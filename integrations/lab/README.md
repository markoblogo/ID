# LAB Integration

## Purpose

Track experiments where profile prompts, model choices, and constraints are varied.

## Minimal Flow

1. Run pre-task hook (`target=lab`).
2. Copy `templates/lab-experiment.md` into `lab/experiments/`.
3. Fill run metadata and mismatch notes.
4. Run post-task hook to append changelog entry.

## Hook Commands

```bash
scripts/run_integration_hook.sh pre_task --owner-id markoblogo --target lab
```

```bash
scripts/run_integration_hook.sh post_task \
  --owner-id markoblogo \
  --session-context "LAB profile experiment" \
  --sections-used "profile.core.md, profile.extended.md" \
  --changes-made "Recorded model mismatch evidence" \
  --open-questions "Need larger sample size"
```
