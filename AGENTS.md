# ID contributor guide

ID is a local CLI for owner-reviewed human context. Markdown profiles are canonical; JSON artifacts are generated transport views.

## Start here

Read `README.md`, `docs/PROTOCOL.md`, `docs/PRIVACY_POLICY_V1.md`, `docs/INTEGRATIONS.md`, and `pyproject.toml`. Keep CLI behavior, schemas, templates, and integration docs aligned.

## Invariants

- Never weaken privacy rules to make an export pass.
- Missing, malformed, mixed, conflicting, or owner-mismatched policies fail closed.
- Supported legacy list policies normalize in memory and remain unchanged on disk.
- Unlisted fields remain local-only.
- Source profiles are never modified by export or integration smoke tests.
- MCP output is resource JSON for an adapter; this package does not run an MCP server.
- SET remains planning-only and agentsgen owns repository instructions.

## Verification

Use a virtual environment, then run:

```bash
python -m pip install ".[dev]" build twine
make validate
make drift-check
make coverage
make release-build
make release-check
```

Before a release, install the wheel with the pinned agentsgen and SET versions and run `scripts/id_release_smoke.py`. Keep package, docs, recorded demo versions, and integration pins synchronized.
