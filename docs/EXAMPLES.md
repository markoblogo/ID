# Golden Examples

## Goal

Show how `ID` works in concrete end-to-end workflows, not just as a protocol description.

Each example focuses on:
- starting inputs
- artifact path
- expected output behavior
- practical value

## 1. Coding Agent

### Input

- `profiles/<owner>/profile.core.md`
- repository task context
- optional `context.compact.json` for transport into another tool

### Flow

1. give the agent the core profile and handshake contract
2. confirm style, constraints, and uncertainty
3. execute coding work with explicit review and safety rules
4. update changelog/profile if the session revealed stable new preferences

### Best artifacts

- markdown source for repo-local work
- `context.compact.json` for portable onboarding

### Typical output gain

- fewer corrective turns about tone, review style, and safety expectations
- faster alignment on what counts as “done”
- easier handoff between coding tools without re-explaining the same constraints

## 2. Literary Editor

### Input

- `profile.core.md` for tone and critique style
- selected `profile.extended.md` sections for taste and recurrent misalignments
- draft text under review

### Flow

1. pass the editor the core profile plus a short handshake
2. include extended-profile sections only when voice and taste matter
3. collect mismatch notes if the editor over-corrects tone or pacing

### Best artifacts

- markdown source profile
- compact export only when moving between tools

### Typical output gain

- more stable editorial voice across sessions
- lower risk of generic “AI rewrite” drift
- easier continuity when changing tools or models

## 3. Market Analyst

### Input

- `profile.core.md`
- `profile.extended.md` heuristics for evidence and decision style
- benchmarkable market-analysis task

### Flow

1. onboard the model with communication and evidence preferences
2. run comparable tasks across tools
3. score outputs against the evaluator protocol
4. compare quality and correction burden with and without `ID`

### Best artifacts

- markdown source for rich context
- benchmark artifacts for comparison

### Typical output gain

- more comparable analyst outputs across tools
- clearer evidence style and better structure fit
- measurable reduction in clarification turns and onboarding overhead

## 4. Cross-Tool Handoff

### Input

- canonical markdown source
- `interop.v1.json`
- `context.compact.json`
- optional `mcp.context.resource.json`

### Flow

1. keep markdown source canonical
2. export transport-specific views
3. validate generated artifacts
4. hand the right artifact to the next tool

### Best artifacts

- `interop.v1.json` for structured portability
- `context.compact.json` for compact prompt/context transfer
- `mcp.context.resource.json` for policy-aware transport wrappers

### Typical output gain

- less dependence on one tool's internal memory model
- explicit loss boundaries
- auditable portability instead of informal copy-paste

## 5. Local Agent Orchestrator

### Input

- markdown source profile
- `privacy-policy.v1.json`
- validated machine artifacts
- repo task and automation context

### Flow

1. validate profile quality, privacy policy, and generated artifacts
2. choose transport form per task class
3. pass policy-aware context into the local orchestrator
4. preserve evidence and drift checks over time

### Best artifacts

- `interop.v1.json`
- `context.compact.json`
- `mcp.context.resource.json`

### Typical output gain

- highest-fidelity multi-tool workflow
- explicit privacy enforcement
- measurable, repeatable behavior instead of ad-hoc orchestration
