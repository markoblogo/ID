# Minimal Profile Guide

## 1. Goal

Lower onboarding friction for new users of `ID`.

Fastest path:
- `make bootstrap-owner OWNER=<owner-id>`
- then follow `docs/QUICKSTART.md`

Use the minimal profile when:
- you want a portable profile in one screen;
- you are onboarding a new agent or tool quickly;
- you do not yet have enough evidence for a trustworthy extended profile.

## 2. Minimal vs Full

### Minimal profile

Use:
- `templates/profile.minimal.md`

Contains only the highest-leverage blocks:
- communication style
- task execution rules
- quality bar
- priority domains
- short tool notes

Best for:
- new coding agent onboarding
- first setup for writing or research assistants
- low-friction portability across tools

### Full profile path

Upgrade path:
1. start with `profile.minimal.md` as the initial source draft;
2. expand into `profile.core.md`;
3. add `profile.extended.md` once repeated patterns and domain workflows are stable;
4. export `interop.v1.json` when portability is needed.

## 3. Recommended Adoption Flow

### Day 0

- run `python3 scripts/bootstrap_owner.py --owner-id <owner-id>`
- fill `profiles/<owner>/profile.minimal.md`
- create a matching handshake
- use it in a real task

### After 3-5 meaningful sessions

- convert recurring guidance into `profile.core.md`
- add changelog entries for corrections

### After repeated domain work

- promote stable workflows and heuristics into `profile.extended.md`

## 4. Keep It Small

Minimal profile rule:
- if the profile cannot fit on one screen without scrolling heavily, it is no longer minimal.

Prefer:
- concrete rules over biography
- task constraints over narrative
- explicit “never do” items over vague style wishes

## 5. Anti-Bloat Rule

Do not add to the minimal profile:
- long historical context
- raw transcript excerpts
- speculative personality claims
- domain-specific workflows better suited for the extended profile
