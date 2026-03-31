# SET Integration

## Purpose

Use orchestration gates so profile freshness and changelog discipline are enforced automatically.

## Required Gates

- pre-run: `pre_task` hook
- post-run: `post_task` hook
- weekly: `weekly_review` hook

## Suggested CI/Automation Calls

```bash
scripts/run_integration_hook.sh pre_task --owner-id markoblogo --target set
```

```bash
scripts/run_integration_hook.sh weekly_review --owner-id markoblogo
```

## Policy Notes

- Non-critical long runs should be blocked if profile is stale beyond TTL.
- Override is allowed only with explicit reduced-confidence marker.
