# Integrations Contract (MVP)

## 1. Purpose

`ID` integrates with external tools through a small hook contract so profile usage is explicit and update discipline is enforced.

Targets covered now:
- `agentsmd`
- `lab`
- `set`

## 2. Hook Runner

Entry point:

```bash
scripts/run_integration_hook.sh <pre_task|post_task|weekly_review> ...
```

Hooks:
- `pre_task`: validate profile + return required profile artifacts for a target tool.
- `post_task`: append standardized changelog entry after meaningful profile-backed work.
- `weekly_review`: generate a health snapshot (profile freshness + raw publish guard).

## 3. Pre-Task Contract

Command:

```bash
scripts/run_integration_hook.sh pre_task --owner-id markoblogo --target agentsmd
```

Expected output includes:
- `profile_core=profiles/<owner>/profile.core.md`
- `handshake=profiles/<owner>/handshake.md`
- `integration_guide=integrations/<target>/README.md`

Behavior:
- runs `validate_profile.py --allow-stale`
- fails if `profile.core.md` or `handshake.md` is missing

## 4. Post-Task Contract

Command:

```bash
scripts/run_integration_hook.sh post_task \
  --owner-id markoblogo \
  --session-context "agents.md coding session" \
  --sections-used "profile.core.md, handshake.md" \
  --changes-made "Updated protocol wording" \
  --open-questions "None"
```

Behavior:
- runs `session_update.py`
- appends one entry to `profiles/<owner>/CHANGELOG.md`

## 5. Weekly Review Contract

Command:

```bash
scripts/run_integration_hook.sh weekly_review --owner-id markoblogo
```

Artifact:
- `data/processed/integration/weekly-review-<owner>-<date>.txt`

Behavior:
- runs profile validation (`allow-stale`)
- runs publish guard (`--all-tracked`)
- stores both outputs in one report

## 6. Target-Specific Notes

- `integrations/agentsmd/README.md`: mandatory handshake before substantive tasks.
- `integrations/lab/README.md`: experiment logging flow for profile/model mismatch analysis.
- `integrations/set/README.md`: orchestration gates (`pre_task`, `post_task`, `weekly_review`).

## 7. Failure Policy

- Missing required profile artifacts: hard fail.
- Stale profile: warning by default in hooks, but can be escalated in CI/pipeline policy.
- Any tool using profile context should trigger `post_task` changelog update (`use implies update`).
