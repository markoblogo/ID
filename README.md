<p align="center">
  <img src="images/IDlogo.png" width="128" alt="ID Protocol logo">
</p>

# ID Protocol — portable context for AI tools

[![CI](https://github.com/markoblogo/ID/actions/workflows/ci.yml/badge.svg)](https://github.com/markoblogo/ID/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/id-protocol)](https://pypi.org/project/id-protocol/)
[![Python](https://img.shields.io/pypi/pyversions/id-protocol)](https://pypi.org/project/id-protocol/)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Keep your working preferences in files you control. ID turns a reviewed profile into compact, privacy-filtered context that can move between AI tools and repositories.

## Try it in five minutes

Requires Python 3.11 or newer.

```sh
uv tool install id-protocol
mkdir my-id-profile && cd my-id-profile
idctl init --owner-id demo
```

Edit `profiles/demo/profile.minimal.md`, then build and inspect the portable output:

```sh
idctl validate --owner-id demo
idctl refresh-soul --owner-id demo
idctl export-compact --owner-id demo
idctl diff --owner-id demo --since 7d
```

The starter profile is provisional until you review it. Use an alias such as `demo` or `my-work-profile`; a legal name is unnecessary. ID does not upload generated files.

## Files and ownership

| File | Role |
| --- | --- |
| `profile.minimal.md` | Small owner-edited starting profile |
| `profile.core.md` | Canonical profile when a fuller source is needed |
| `profile.extended.md` | Optional detailed workflows and context |
| `privacy-policy.v1.json` | Per-field export permissions |
| `handshake.md` | Concise rules for applying context |
| `soul.md` | Short derived bootstrap for an agent |
| `context.compact.json` | Privacy-filtered portable context |
| `mcp.context.resource.json` | Resource payload for an external MCP adapter |

Markdown profiles remain the source of truth. Generated JSON is a transport view and may omit nuance. The package is a local CLI; it does not provide an MCP server or synchronize vendor accounts.

## Privacy behavior

Compact and MCP resource exports require a valid policy whose `owner_id` matches the requested profile. Unlisted fields stay local-only. Missing, malformed, mixed, conflicting, or owner-mismatched policies block export.

Legacy list policies from earlier releases are normalized in memory during validation and export. Their source files remain unchanged and their restrictions remain effective. `--allow-unfiltered` only permits a missing policy in a reviewed legacy workflow; it cannot bypass an invalid policy.

Review the resulting export before attaching it to another tool. See the [privacy model](docs/PRIVACY.md), [policy schema](docs/PRIVACY_POLICY_V1.md), and [threat model](docs/THREAT_MODEL.md).

## ABVX toolchain

| Product | Responsibility | Tested release |
| --- | --- | --- |
| ID | Human preferences and operating constraints | 0.5.2 |
| [agentsgen](https://github.com/markoblogo/AGENTS.md_generator) | Repository instructions and commands | 0.5.0 |
| [SET](https://github.com/markoblogo/SET) | Review-first workflow planning and exports | 0.4.0 |
| [abvx-agent-skills](https://github.com/markoblogo/abvx-agent-skills) | Optional reusable workflows | 0.15.0 |

These remain independently installable. ID does not install companions or grant tool permissions.

For a repository that already contains a reviewed ID profile:

```sh
idctl install-set-hook --path .
```

The adapter returns owner-local bootstrap pointers to SET and preserves an existing custom hook. See the [SET integration guide](integrations/set/README.md).

## Evidence

[Three reproducible demos](docs/RELEASE_DEMOS.md) exercise installed onboarding, policy-filtered omission, legacy-policy compatibility, and the agentsgen/SET handoff with synthetic data. They measure local CLI behavior and runtime, not AI answer quality.

The [historical benchmark snapshot](docs/benchmark-snapshot.md) is a small checked-in sample with explicit limits. AI-client behavior still depends on each client's configuration and context rules.

## Develop

```sh
git clone https://github.com/markoblogo/ID.git
cd ID
python -m venv .venv
. .venv/bin/activate
python -m pip install ".[dev]" build twine
make validate
make drift-check
make coverage
make release-build
make release-check
```

Start with the [documentation index](docs/README.md), [protocol](docs/PROTOCOL.md), [integration boundaries](docs/INTEGRATIONS.md), and [contributing guide](CONTRIBUTING.md). Use synthetic profiles in public issues and pull requests.

<!-- ABVX:ECOSYSTEM:BEGIN -->
## ABVX ecosystem

- [AGENTS.md_generator](https://agentsmd.abvx.xyz/) — Exports reviewed context for repository guidance. Current release: `v0.5.1`.
- [AGENTS.md_generator](https://agentsmd.abvx.xyz/) — Keeps repository guidance and machine-readable context current. Current release: `v0.5.1`.
- [abvx-agent-skills](https://abvx.xyz/work/abvx-agent-skills) — Uses shared, reviewable agent capabilities during maintenance. Current release: `v0.15.0`.

_This block is generated from the reviewed ABVX ecosystem registry._
<!-- ABVX:ECOSYSTEM:END -->
