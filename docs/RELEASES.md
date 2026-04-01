# Releases

`ID` now has an installable lightweight CLI surface from source.

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

## Current Release Posture

- installable from source via `pip install .`
- lightweight wrapper CLI via `idctl`
- no PyPI, Homebrew, or npm publication yet

## Recommended Next Release Steps

1. Create tagged GitHub releases.
2. Publish an sdist and wheel.
3. Decide whether `idctl` stays thin or grows a richer UX.
