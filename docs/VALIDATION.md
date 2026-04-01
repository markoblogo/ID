# Validation and Session Automation (MVP)

## 1. Validate Profiles

Run metadata + freshness checks:

- `python3 scripts/validate_profile.py --owner-id markoblogo`

Recommended progression:
- validate a minimal/core profile first;
- expand to the extended profile only after the minimal/core layer survives real sessions.

Strict publish safety check (recommended before push):

- `python3 scripts/validate_profile.py --check-raw-staged --check-raw-tracked`

Allow stale profiles as warnings during transition:

- `python3 scripts/validate_profile.py --allow-stale`

## 2. Raw Publish Guard

Fast guard for CI/pre-push:

- staged only: `python3 scripts/check_publish_guard.py`
- include tracked: `python3 scripts/check_publish_guard.py --all-tracked`

## 3. Post-Session CHANGELOG Update

Append a standardized changelog entry:

```bash
python3 scripts/session_update.py \
  --owner-id markoblogo \
  --session-context "Profile-backed coding session" \
  --sections-used "Communication Signals, Task Execution Rules" \
  --changes-made "Refined privacy constraints" \
  --open-questions "Need image-model preference block"
```

This updates:
- `profiles/<owner-id>/CHANGELOG.md`
