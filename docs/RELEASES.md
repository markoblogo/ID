# Releases

`ID` now has a normal source-build release path and a lightweight installed CLI surface.

## Install From Source

```bash
pip install .
```

This installs:

```bash
idctl
```

## Current CLI Surface

Examples:

```bash
idctl bootstrap-owner --owner-id <owner-id>
idctl refresh-soul --owner-id <owner-id>
idctl export-compact --owner-id <owner-id>
idctl export-mcp --owner-id <owner-id>
idctl validate-observed
idctl metrics
```

The CLI is intentionally thin. It wraps the existing reference scripts rather than
introducing a second execution model.

## Build Release Artifacts Locally

```bash
make release-build
make release-check
```

This produces:

```bash
dist/*.tar.gz
dist/*.whl
```

`make release-check` runs `twine check` against the built artifacts.

If your system Python is externally managed, use an isolated virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install build twine
make PYTHON=.venv/bin/python release-build
make PYTHON=.venv/bin/python release-check
```

## GitHub Release Flow

Normal release flow:

1. bump the project version in `pyproject.toml`
2. commit the version change
3. create and push a tag such as `v0.2.0`
4. GitHub Actions runs the release workflow
5. the workflow:
   - runs `make validate`
   - builds `sdist` and `wheel`
   - checks metadata with `twine`
   - attaches `dist/*` to the GitHub release

Workflow file:

```text
.github/workflows/release.yml
```

## PyPI Publishing Flow

PyPI publishing is separated from GitHub release creation.

Workflow file:

```text
.github/workflows/pypi-publish.yml
```

Flow:

1. a GitHub release is published
2. the PyPI workflow downloads the release assets
3. the workflow publishes them to PyPI via trusted publishing

Before enabling real publication, configure:

1. the final package name on PyPI
2. a trusted publisher for `markoblogo/ID`
3. the `pypi` GitHub environment, ideally with approval protection

Current (active) PyPI and MCP configuration:

- package name: `id-protocol`
- GitHub owner: `markoblogo`
- GitHub repository: `ID`
- workflow file: `.github/workflows/pypi-publish.yml`
- environment: `pypi`
- GitHub Release workflow file: `.github/workflows/release.yml`

PyPI workflow now performs MCP registry publication after a successful PyPI upload.
It uses `scripts/build_registry_server_json.py` to generate a registry-compatible `server.json`
and authenticates with `mcp-publisher login github-oidc`, so no dedicated registry JWT secret is required.

This separation is intentional:
- GitHub release remains the canonical first publication step
- PyPI publication stays auditable and can be approval-gated
- MCP registry publication happens only after the corresponding package version is live on PyPI

## Current Release Posture

- installable from source via `pip install .` or built artifacts in `dist/`
- lightweight wrapper CLI via `idctl`
- tagged GitHub release flow for `sdist`/`wheel`
- PyPI publish flow is live via trusted publishing (`id-protocol-pypi-publish`)
- no Homebrew or npm publication yet

## Recommended Next Release Steps

1. Decide whether Homebrew or `pipx` should be a first-class install path.
2. Decide whether `idctl` stays thin or grows a richer UX.
