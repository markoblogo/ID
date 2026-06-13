# ID Protocol

[![GitHub Release](https://img.shields.io/github/v/release/markoblogo/ID)](https://github.com/markoblogo/ID/releases)
[![PyPI](https://img.shields.io/pypi/v/id-protocol)](https://pypi.org/project/id-protocol/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/markoblogo/ID/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/id-protocol)](https://pypi.org/project/id-protocol/)
[![CI](https://github.com/markoblogo/ID/actions/workflows/ci.yml/badge.svg)](https://github.com/markoblogo/ID/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/markoblogo/ID/branch/main/graph/badge.svg)](https://codecov.io/gh/markoblogo/ID)

<p>
  <img src="images/IDlogo.png" alt="ID Protocol Logo" width="240">
</p>

`ID` turns a person into portable AI context with explicit freshness, trust, provenance, and privacy rules.
<!-- mcp-name: io.github.markoblogo/id -->

It is not another assistant. It is the profile and contract layer that can travel across tools.

## What It Covers

- canonical owner-managed profile files
- compact derived `soul.md` for fast agent bootstrap
- portable interop artifacts (`context.compact`, `interop.v1`, `mcp`)
- validation, freshness, and publish-safety checks
- integration points for `SET`, `agentsgen`, and other repo workflows

## Start In 5 Minutes

Install:

```bash
brew install markoblogo/tap/id-protocol
```

Bootstrap:

```bash
idctl init --owner-id <owner-id>
idctl refresh-soul --owner-id <owner-id>
make validate
make compact
```

You end up with:

- `profile.minimal.md` as the first owner checkpoint
- `soul.md` as the short reviewed handoff layer
- `context.compact.json` as the portable compact artifact

## Core Files

Source of truth:

- `profiles/<owner>/profile.minimal.md`
- `profiles/<owner>/profile.core.md`
- `profiles/<owner>/profile.extended.md`
- `profiles/<owner>/CHANGELOG.md`

Derived layers:

- `profiles/<owner>/soul.md`
- `profiles/<owner>/context.compact.json`
- `profiles/<owner>/interop.v1.json`
- `profiles/<owner>/mcp.context.resource.json`

## Why This Exists

- system prompts are fragile and usually copied by hand
- chat-native memory is product-siloed and hard to audit
- repo instructions help per repo, not across tools or roles
- `ID` keeps user context explicit, versioned, reviewable, and portable

`soul.md` exists because the full profile stack is often too heavy for the first pass. It gives agents a short bootstrap surface without replacing the canonical profile files.

## Ecosystem Role

- `ID` owns portable human context
- `agentsgen` owns repo-scoped agent context
- `SET` can orchestrate both layers

Practical rule:

- use `ID` for the human
- use `agentsgen` for the repository
- use `SET` when you want orchestration around both

## Quick Paths

- `Lite`: `docs/LITE.md`
- `Share`: `docs/SHARE.md`
- `Bench`: `docs/BENCH.md`
- `Soul`: `docs/SOUL.md`
- `Integrations`: `docs/INTEGRATIONS.md`
- `Releases`: `docs/RELEASES.md`
- full docs index: `docs/README.md`

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
- profiles/markoblogo/profile.core.md: score=0.0 age=74 ttl=14
- profiles/markoblogo/profile.extended.md: score=0.0 age=73 ttl=30
```

<!-- METRICS_SNIPPET_END -->

## Current CLI Surface

```bash
idctl init --owner-id <owner-id>
idctl refresh-soul --owner-id <owner-id>
idctl validate
idctl export-compact --owner-id <owner-id>
idctl export-interop --owner-id <owner-id>
idctl export-mcp --owner-id <owner-id>
```

## Current Status

Today `ID` functions as:

- a protocol/spec reference
- a validated tooling reference
- a compact onboarding path
- an installable CLI package on PyPI/Homebrew

Latest release: `v0.3.0` adds the derived `soul.md` layer and refresh flow.
