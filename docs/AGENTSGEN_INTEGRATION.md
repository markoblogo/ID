# AGENTS.md Generator Integration

This document makes the `ID` and `agentsgen` relationship explicit at the repo-contract level.

## Boundary

- `ID` owns portable human context, freshness, privacy, and handshakes.
- `agentsgen` owns repo-scoped agent context and command manifests.
- `SET` can orchestrate both layers, but the bridge should also work without `SET`.

## Repo-local handoff contract

When a repository runs `agentsgen pack --autodetect`, it can publish `docs/ai/id-context.json`.

That file is the repo-local handoff surface for `ID`-compatible workflows. It should point at the repo artifacts that matter most for execution:

- `AGENTS.md`
- `RUNBOOK.md`
- `agents.entrypoints.json`
- `docs/ai/how-to-run.md`
- `docs/ai/how-to-test.md`
- `docs/ai/architecture.md`
- `docs/ai/data-contracts.md`
- optional `repomap`, `graph`, `agents.knowledge.json`, and proof-loop task artifacts when present

## Recommended flow

1. Load the owner profile and handshake from `ID`.
2. If present, load `profiles/<owner>/soul.md` as the fast human-context bootstrap layer.
3. Load `docs/ai/id-context.json` from the active repository.
4. Merge human context from `ID` with repo context from `agentsgen`.
5. If orchestration is present, let `SET` call `pre_task` and `weekly_review` around the repo workflow.

## Non-goals

- `docs/ai/id-context.json` does not replace `profile.core.md`, `profile.extended.md`, or interop exports.
- `soul.md` does not replace the canonical source profile files; it is a compact derived layer.
- `agentsgen` does not own user preferences or privacy policy.
- `ID` does not replace repo-local contracts such as `AGENTS.md`.

## Practical summary

Use `ID` for the human.
Use `agentsgen` for the repository.
Use `SET` when you want one orchestration entrypoint for both.
