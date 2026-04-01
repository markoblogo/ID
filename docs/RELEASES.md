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

## Current Release Posture

- installable from source via `pip install .` or built artifacts in `dist/`
- lightweight wrapper CLI via `idctl`
- tagged GitHub release flow for `sdist`/`wheel`
- no PyPI, Homebrew, or npm publication yet

## Recommended Next Release Steps

1. Publish artifacts to PyPI once the package name and maintenance policy are stable.
2. Decide whether Homebrew or `pipx` should be a first-class install path.
3. Decide whether `idctl` stays thin or grows a richer UX.
