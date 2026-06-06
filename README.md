# ID Protocol

[![GitHub Release](https://img.shields.io/github/v/release/markoblogo/ID)](https://github.com/markoblogo/ID/releases)
[![PyPI](https://img.shields.io/pypi/v/id-protocol)](https://pypi.org/project/id-protocol/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/markoblogo/ID/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/id-protocol)](https://pypi.org/project/id-protocol/)
[![CI](https://github.com/markoblogo/ID/actions/workflows/ci.yml/badge.svg)](https://github.com/markoblogo/ID/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/markoblogo/ID/branch/main/graph/badge.svg)](https://codecov.io/gh/markoblogo/ID)

![ID Protocol Logo](images/IDlogo.png)

`ID` turns a person into a portable AI context that travels between tools with explicit freshness, trust, and privacy rules.
<!-- mcp-name: io.github.markoblogo/id -->

Positioning:
- `ID` is **not another assistant**. It is the protocol layer that keeps context explicit, portable, and auditable.
- It complements `SET`, `agentsmd`, and other orchestrators by making context, contracts, and hooks first-class.

### Start in 5–10 minutes

Install with Homebrew:

```bash
brew install markoblogo/tap/id-protocol
```

1. `idctl init --owner-id <owner-id>`
2. fill `profiles/<owner>/profile.minimal.md`
3. `make validate`
4. `make compact`

Result:
- immediate AI-ready portable context
- one concrete checkpoint (`profile.minimal.md`)
- generated artifact (`context.compact.json`)

### Quick path

- `Lite` path: minimal setup, get started fast → `docs/LITE.md`
- `Share` path: multi-tool portability → `docs/SHARE.md`
- `Bench` path: evidence and claims → `docs/BENCH.md`

### Comparative note

- `Copilot`, `Cursor`, and `Continue` generate local prompt memories.
- `ID` gives a stable externalized profile and contract that those tools can consume.

<!-- METRICS_SNIPPET_START -->
### Live Public Metrics

Runs analyzed: `4`

| Metric | Value | Meaning |
| --- | --- | --- |
| onboarding latency | 1.15 | Less is better |
| clarification turns | 0.85 | Less hand-offs |
| task success | 0.6 | Higher is better |
| alignment index | 18.3 | Higher is better |

Profile freshness score (owner `markoblogo`): `0.0`

```
Key artifacts:
- profiles/markoblogo/profile.core.md: score=0.0 age=67 ttl=14
- profiles/markoblogo/profile.extended.md: score=0.0 age=66 ttl=30
```

<!-- METRICS_SNIPPET_END -->

## Orchestration status

`ID` now has a real execution role inside the wider ABVX toolchain:

- `SET` can orchestrate repo-local `ID` hooks in compatible repositories
- current CI-safe hooks are `pre_task` and `weekly_review`
- `ID` stays the context/protocol layer, while `SET` stays the orchestration layer
- `agentsgen` remains the repo-docs/runtime companion, not a replacement for portable human context

Practical consequence:
- if a repo is `ID`-compatible, `SET` can validate or refresh human-context boundaries before and after the main repo workflow
- if a repo only needs repo-scoped agent docs, `agentsgen` is enough on its own

Why this beats ad-hoc prompts or chat memory in some workflows:
- `system prompts` are fragile and usually copied by hand across tools;
- chat-native memory is siloed inside one product and hard to audit;
- project instructions help per repo, but not across roles like writing, research, or multi-tool orchestration;
- `ID` makes preferences, constraints, freshness, privacy, and portability explicit and versioned.

Evidence surface:
- `docs/PROOF.md` (claim pack and caveats)
- `benchmarks/runs/public-metrics.md` (live utility summary)
- `docs/MEASUREMENT.md` and `docs/EVALUATOR_PROTOCOL.md` (method)
- `docs/EVIDENCE_POLICY.md` (evidence rules)

Ecosystem map:
- `docs/ECOSYSTEM.md`
- `docs/INTEGRATIONS.md`
- docs entrypoint index: `docs/README.md`

Release/install:
- `docs/RELEASES.md`

## Choose One Path

### 1. `ID Lite`

Use this if you want the smallest practical entrypoint.

You get:
- a starter profile
- a handshake
- a privacy policy starter
- a compact portable artifact

Start here:
- `docs/LITE.md`

### 2. `ID Share`

Use this if you want to move context safely between tools or people.

You get:
- validated interop/compact/MCP artifacts
- explicit privacy policy
- documented loss boundaries

Start here:
- `docs/SHARE.md`

### 3. `ID Bench`

Use this if you want proof that `ID` actually helps.

You get:
- benchmark runs
- with-vs-without-ID comparisons
- public metrics
- proof summaries with caveats

Start here:
- `docs/BENCH.md`

## End-to-End Scenarios

### 1. New Coding Agent

Input:
- `profiles/<owner>/profile.core.md`
- `profiles/<owner>/profile.extended.md`
- repo context for the actual task

Flow:
1. run pre-task hook or hand the agent the core profile + handshake.
2. agent summarizes understanding, constraints, and uncertainty.
3. agent executes coding work under explicit style and safety rules.
4. after the session, changelog and profile updates are recorded if needed.

Output:
- faster alignment on review style, verbosity, safety, and tooling assumptions
- fewer corrective turns than repeating the same guidance manually in each repo

### 2. Literary Editor

Input:
- core profile for tone, critique style, and hard constraints
- extended profile for taste, recurrent misalignments, and known-good phrasing
- draft text under review

Flow:
1. editor model reads the profile-backed handshake.
2. critique is generated in the preferred format and tone.
3. mismatch notes are captured if the editor over-corrects voice or pacing.

Output:
- more stable editorial voice across sessions and tools
- lower risk of generic “AI rewrite” drift

### 3. Market Analyst

Input:
- core profile with communication preferences and risk constraints
- extended profile with domain heuristics and decision rules
- source material for the market question

Flow:
1. analyst model uses the profile to choose structure, brevity, and evidence style.
2. benchmarkable outputs can be compared across tools on the same task set.
3. results are scored for style fit, constraint adherence, and usefulness.

Output:
- comparable outputs across models instead of one-off subjective impressions
- easier onboarding for a new model without rebuilding context from scratch

### 4. Cross-Tool Handoff

Input:
- markdown source profile
- generated `profiles/<owner>/interop.v1.json`
- redaction policy when sharing externally

Flow:
1. export markdown source into interop artifact.
2. validate the artifact against schema and repo rules.
3. hand the redacted or full package to another tool, wrapper, or automation path.

Output:
- portable context with explicit loss boundaries
- less dependence on one chat product's internal memory model

## Repository Structure

```text
.
├── benchmarks/
│   ├── tasks/
│   └── runs/
├── data/
│   ├── raw/
│   ├── normalized/
│   └── processed/
├── docs/
│   ├── PROTOCOL.md
│   ├── OPERATIONS.md
│   ├── INGEST_SOURCES.md
│   ├── PRIVACY.md
│   ├── VALIDATION.md
│   ├── INTEGRATIONS.md
│   ├── BENCHMARK.md
│   ├── INTEROP_V1.md
│   ├── HARDENING.md
│   └── ROADMAP.md
├── integrations/
│   ├── agentsmd/
│   ├── lab/
│   └── set/
├── lab/
│   └── experiments/
├── profiles/
├── schemas/
├── scripts/
├── templates/
└── README.md
```

## Phase Status

- Phase 0 (bootstrap): done
- Phase 1 (ingest + extractor MVP): done
- Phase 2 (privacy/redaction): done
- Phase 3 (validation automation): done
- Phase 4 (integrations): done
- Phase 5 (benchmark + interop): done
- Phase 6 (hardening): done
- Phase 7 (expansion): done

## Current Maturity

Today this repository functions as:
- a protocol/spec reference
- a validated tooling reference
- a benchmark/evidence reference
- a lightweight onboarding entrypoint
- an installable lightweight CLI surface

It is no longer only an internal profile format or documentation experiment.

## Ecosystem Status

### `ID` and `lab.abvx`

- repo: [markoblogo/lab.abvx](https://github.com/markoblogo/lab.abvx)
- landing: [lab.abvx.xyz](https://lab.abvx.xyz/)
- current relationship:
  - `lab.abvx` is the broader experiment/catalog surface
  - `ID` sits in that ecosystem as a protocol/reference implementation for portable human-AI context
  - `lab.abvx.xyz` should be treated as an adjacent discovery or catalog surface, not the canonical protocol source of truth

### `ID` and `AGENTS.md Generator`

- repo: [markoblogo/AGENTS.md_generator](https://github.com/markoblogo/AGENTS.md_generator)
- landing: [agentsmd.abvx.xyz](https://agentsmd.abvx.xyz/)
- current relationship:
  - `AGENTS.md Generator` is companion tooling for generating and maintaining agent-facing repo instructions
  - `ID` is the person/tool interaction protocol layer
  - they complement each other:
    - `ID` defines portable human-AI context
    - `AGENTS.md Generator` helps produce repo-scoped agent guidance
  - `agentsmd.abvx.xyz` is the landing/product surface for that adjacent toolchain, not the `ID` protocol home

### `ID` and `SET`

- repo: [markoblogo/SET](https://github.com/markoblogo/SET)
- current relationship:
  - `SET` is the orchestration/execution layer
  - `ID` is now a real repo-local hook and protocol companion inside that orchestration path
  - practical boundary:
    - `ID` answers "what context should follow the human across tools?"
    - `SET` answers "how should repo workflows execute those tools and hooks?"

### `ID` and `DecisionMap`

- repo: [markoblogo/decision-map](https://github.com/markoblogo/decision-map)
- current relationship:
  - `DecisionMap` is a standalone decision/strategy protocol + prompt toolkit
  - `ID` can be used as an optional portable context layer for long-running decision work
  - no hard dependency: `DecisionMap` remains usable with any LLM without `ID`

### Practical Summary

If you need:
- protocol and portable context: start with `ID`
- repo-scoped agent instruction generation: use `AGENTS.md Generator`
- orchestration and workflow execution: use `SET`

## Specification And Releases

- protocol/spec surface: `spec/`
- versioning and conformance: `docs/VERSIONING.md`, `spec/CONFORMANCE.md`
- releases and install: `docs/RELEASES.md`
- broader experiment catalog / ecosystem discovery: use `lab.abvx`
- orchestration/execution workflows: use `SET`

## Specification

- current protocol docs live under `docs/`
- versioned standard surface lives under `spec/`
- current version index: `spec/v0.2/README.md`
- conformance model: `spec/CONFORMANCE.md`
- change history: `spec/CHANGELOG.md`
- proposal process: `spec/RFC/README.md`
- versioning semantics: `docs/VERSIONING.md`
- compatibility matrix: `docs/COMPATIBILITY.md`
- observed behavior notes: `docs/OBSERVED_BEHAVIOR.md`
- observed behavior evidence: `evidence/observed-behavior/*.json`
- evidence maintenance policy: `docs/EVIDENCE_POLICY.md`
- compact target mapping: `docs/CONTEXT_JSON_MAPPING.md`

## Start Small

Recommended onboarding path:
- bootstrap a starter set with `python3 scripts/bootstrap_owner.py --owner-id <owner-id>`
- or `make bootstrap-owner OWNER=<owner-id>`
- start with `templates/profile.minimal.md`
- then promote stable guidance into `profiles/<owner>/profile.core.md`
- add `profile.extended.md` only after repeated workflows and misalignments are clear

Guide:
- `docs/MINIMAL_PROFILE.md`
- `docs/QUICKSTART.md`

## Ingest + Extract

- put exports to `data/raw/<source>/`
- normalize into `data/normalized/<source>/`
- run: `python3 scripts/extract_profile.py --owner-id <owner-id>`

## Privacy + Safe-Share

- policy: `docs/PRIVACY.md`
- machine-readable policy: `docs/PRIVACY_POLICY_V1.md`
- threat model: `docs/THREAT_MODEL.md`
- validate policy: `python3 scripts/validate_privacy_policy.py --owner-id <owner-id>`
- run: `python3 scripts/redact_for_sharing.py`
- review: `data/processed/redaction-report.json`

## Validation + Changelog Automation

- validate: `python3 scripts/validate_profile.py --owner-id <owner-id>`
- publish guard: `python3 scripts/check_publish_guard.py --all-tracked`
- post-session entry:
  - `python3 scripts/session_update.py --owner-id <owner-id> --session-context "..." --sections-used "..." --changes-made "..."`

## Integrations Hooks

- pre-task:
  - `scripts/run_integration_hook.sh pre_task --owner-id <owner-id> --target agentsmd`
- post-task:
  - `scripts/run_integration_hook.sh post_task --owner-id <owner-id> --session-context "..." --sections-used "..." --changes-made "..."`
- weekly review:
  - `scripts/run_integration_hook.sh weekly_review --owner-id <owner-id>`

## Benchmark + Interop

- benchmark guide: `docs/BENCHMARK.md`
- evaluator protocol: `docs/EVALUATOR_PROTOCOL.md`
- public utility positioning: `docs/WHY_ID.md`
- golden examples: `docs/EXAMPLES.md`
- proof summary: `docs/PROOF.md`
- run aggregation: `python3 scripts/benchmark_report.py --run-id <run-id>`
- trend report across runs: `python3 scripts/benchmark_trend_report.py`
- public metrics report: `python3 scripts/benchmark_public_report.py`
- initialize benchmark run: `python3 scripts/benchmark_init_run.py --run-id <run-id> --tool <tool> --owner-id <owner-id> --profile-version <version>`
- validate benchmark run: `python3 scripts/benchmark_validate_run.py --run-id <run-id>`
- interop v1 guide: `docs/INTEROP_V1.md`
- compatibility guide: `docs/COMPATIBILITY.md`
- compact export contract: `docs/CONTEXT_JSON_MAPPING.md`
- public metrics guide: `docs/MEASUREMENT.md`
- threat model: `docs/THREAT_MODEL.md`
- compact exporter: `python3 scripts/export_context_compact.py --owner-id <owner-id>`
- compact validator: `python3 scripts/validate_context_compact.py --owner-id <owner-id>`
- compact import draft: `python3 scripts/import_context_compact.py --owner-id <owner-id>`
- export interop json: `python3 scripts/export_interop_v1.py --owner-id <owner-id>`
- interop artifact policy: `profiles/<owner>/interop.v1.json` is versioned and must be regenerated after profile changes
- validate interop json: `python3 scripts/validate_interop_v1.py --owner-id <owner-id>`
- MCP import draft: `python3 scripts/import_mcp_resource.py --owner-id <owner-id>`
- shortcut commands:
  - `make validate`
  - `make bootstrap-owner OWNER=<owner-id>`
  - `make interop`
  - `make compact`
  - `make mcp`
  - `make privacy-policy`
  - `make observed-behavior`
  - `make metrics`
  - `make trend`

## Hardening

- hardening guide: `docs/HARDENING.md`
- CI workflow: `.github/workflows/ci.yml`
- baseline example: `benchmarks/runs/baseline-2026-03-31-codex/`
