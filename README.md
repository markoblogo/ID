# ID — portable context for AI tools

Keep your working preferences in reviewed files. Reuse them across projects and AI tools, and inspect what changed before sharing.

[![CI](https://github.com/markoblogo/ID/actions/workflows/ci.yml/badge.svg)](https://github.com/markoblogo/ID/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/id-protocol)](https://pypi.org/project/id-protocol/)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

ID gives you a small owner profile, a derived `soul.md`, portable JSON exports,
privacy rules, and a semantic diff. You choose which files an AI tool receives.

## Start with one profile

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).
Run in a private working directory:

```sh
uv tool install id-protocol
idctl init --owner-id demo
```

Edit `profiles/demo/profile.minimal.md`: language, level of detail, working rules,
and what a good result means to you. The starter is **provisional** until you review it.
Use an owner ID such as `demo` or `my-work-profile`; a real name is unnecessary.

```sh
idctl validate --owner-id demo
idctl refresh-soul --owner-id demo
idctl export-interop --owner-id demo
idctl export-compact --owner-id demo
idctl validate-compact --owner-id demo
```

These commands work from an installed package, outside this repository. No Makefile,
API key, central registry, or paid service is required.
Validation checks structure and freshness; it cannot decide whether the profile reflects you.

## What you get

| File | Purpose |
| --- | --- |
| `profile.minimal.md` | Owner-edited starting point |
| `privacy-policy.v1.json` | Rules for filtered exports |
| `handshake.md` | Instructions for confirming context |
| `soul.md` | Short derived bootstrap; refresh after source edits |
| `context.compact.json` | Portable, policy-filtered context |

Add `profile.core.md` and `profile.extended.md` when you need more detail.
If core exists, it takes precedence over minimal for interop exports.
The extended profile is optional. Init refuses to overwrite existing starter files.

## Review before sharing

```sh
idctl diff --owner-id demo --since 7d
```

Diff uses Git history; commit reviewed source changes if you want version comparisons.
`interop.v1.json` and `soul.md` are local derived context, **not privacy-filtered sharing bundles**.
Review your policy and the resulting compact export before giving it to another tool.
Missing, invalid, or mismatched policies block compact/MCP export. The explicit
`--allow-unfiltered` option permits a missing policy for a reviewed legacy workflow;
it does not bypass an invalid policy.

Generating or exporting a file does not upload it. Source profiles remain under your control.

## Use with agentsgen and SET

| Product | Owns | Tested release |
| --- | --- | --- |
| ID | Human preferences and operating constraints | 0.5.0 |
| [agentsgen](https://github.com/markoblogo/AGENTS.md_generator) | Repository commands and instructions | 0.5.0 |
| [SET](https://github.com/markoblogo/SET) | Workflow presets and planning exports | 0.3.1 |
| [abvx-agent-skills](https://github.com/markoblogo/abvx-agent-skills) | Optional reusable agent workflows | 0.14.0, optional pairing |

All remain separate products. ID does not install the others automatically.
The first three versions are exercised together in release CI; skills are an optional
workflow reference and are not part of the executable compatibility test.

For a repository that already has ID profiles:

```sh
idctl install-set-hook --path .
```

This creates a small repo-local adapter for SET. It requires `idctl` on PATH,
preserves an existing custom hook, and resolves bootstrap files inside the selected
owner directory. [Complete SET setup](integrations/set/README.md).

## Evidence and compatibility

[Three reproducible demos](docs/RELEASE_DEMOS.md) verify installed onboarding,
privacy-policy omissions, and the agentsgen/SET handoff with synthetic profiles.
They measure CLI behavior and runtime, not AI task quality.

AI-client loading depends on each client's configuration. ID exports files for
manual attachment or an adapter; it does not automatically synchronize ChatGPT,
Claude, Cursor, or other clients. `export-mcp` creates resource JSON for an adapter;
this package does not run an MCP stdio or HTTP server.

Historical benchmark runs are available as a [dated snapshot](docs/benchmark-snapshot.md).
They are a small sample, not a general performance guarantee.

## Explore or contribute

- [Core protocol](spec/) and [full documentation](docs/README.md).
- [Profile layers](docs/SOUL.md), [sharing](docs/SHARE.md), and [semantic diffs](docs/IDENTITY_DIFF.md).
- [Integration boundaries](docs/INTEGRATIONS.md) and [release notes](docs/RELEASES.md).
- [Contributing](CONTRIBUTING.md): include a synthetic reproduction, package version, and expected/actual output.

For source development: install `.[dev]`, then run `make validate` and `make coverage`.
Keep real private profiles outside this public repository.
