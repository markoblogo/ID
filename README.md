# ID Protocol

![ID Protocol Logo](images/IDlogo.png)

`ID` is a repository standard for portable human-AI interaction context.

Main idea:
- any AI should quickly understand how to work with a specific person;
- context has depth levels: short, extended, full;
- using context implies responsibility to keep it updated.

Why this beats ad-hoc prompts or chat memory in some workflows:
- `system prompts` are fragile and usually copied by hand across tools;
- chat-native memory is siloed inside one product and hard to audit;
- project instructions help per repo, but not across roles like writing, research, or multi-tool orchestration;
- `ID` makes preferences, constraints, freshness, privacy, and portability explicit and versioned.

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

## Ecosystem Links

- SET orchestration: https://github.com/markoblogo/SET
- Lab catalog: https://github.com/markoblogo/lab.abvx
- agentsgen toolchain: https://github.com/markoblogo/AGENTS.md_generator

## Specification

- current protocol docs live under `docs/`
- versioned standard surface lives under `spec/`
- current version index: `spec/v0.1/README.md`
- conformance model: `spec/CONFORMANCE.md`
- change history: `spec/CHANGELOG.md`
- proposal process: `spec/RFC/README.md`
- compatibility matrix: `docs/COMPATIBILITY.md`
- compact target mapping: `docs/CONTEXT_JSON_MAPPING.md`

## Start Small

Recommended onboarding path:
- start with `templates/profile.minimal.md`
- then promote stable guidance into `profiles/<owner>/profile.core.md`
- add `profile.extended.md` only after repeated workflows and misalignments are clear

Guide:
- `docs/MINIMAL_PROFILE.md`

## Ingest + Extract

- put exports to `data/raw/<source>/`
- normalize into `data/normalized/<source>/`
- run: `python3 scripts/extract_profile.py --owner-id <owner-id>`

## Privacy + Safe-Share

- policy: `docs/PRIVACY.md`
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
- run aggregation: `python3 scripts/benchmark_report.py --run-id <run-id>`
- trend report across runs: `python3 scripts/benchmark_trend_report.py`
- initialize benchmark run: `python3 scripts/benchmark_init_run.py --run-id <run-id> --tool <tool> --owner-id <owner-id> --profile-version <version>`
- validate benchmark run: `python3 scripts/benchmark_validate_run.py --run-id <run-id>`
- interop v1 guide: `docs/INTEROP_V1.md`
- compatibility guide: `docs/COMPATIBILITY.md`
- compact export contract: `docs/CONTEXT_JSON_MAPPING.md`
- compact exporter: `python3 scripts/export_context_compact.py --owner-id <owner-id>`
- compact validator: `python3 scripts/validate_context_compact.py --owner-id <owner-id>`
- export interop json: `python3 scripts/export_interop_v1.py --owner-id <owner-id>`
- interop artifact policy: `profiles/<owner>/interop.v1.json` is versioned and must be regenerated after profile changes
- validate interop json: `python3 scripts/validate_interop_v1.py --owner-id <owner-id>`
- shortcut commands:
  - `make validate`
  - `make interop`
  - `make trend`

## Hardening

- hardening guide: `docs/HARDENING.md`
- CI workflow: `.github/workflows/ci.yml`
- baseline example: `benchmarks/runs/baseline-2026-03-31-codex/`
