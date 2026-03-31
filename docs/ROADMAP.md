# ID Roadmap (Draft)

## Phase 0: Bootstrap (done)

- protocol spec drafted;
- operations playbook drafted;
- templates and schemas added.

## Phase 1: Real Profile Pilot

- create first real profile under `profiles/markoblogo/`;
- run 10+ sessions with 2-3 different AI tools;
- collect mismatch logs and profile corrections.

## Phase 2: Tooling

- add CLI validation for profile metadata freshness;
- add JSON export from Markdown profile sections;
- add redaction command for external sharing.

## Phase 3: Integrations

- `agents.md`: automatic injection of `profile.core.md` at session start;
- `LAB`: experiment registry for prompt/profile variants;
- `SET`: orchestration checks for stale profiles and mandatory changelog update.

## Phase 4: Community/Interop

- publish stable `v1` field naming;
- provide migration notes for `v0` to `v1`;
- define extension slots for domain-specific profiles.
