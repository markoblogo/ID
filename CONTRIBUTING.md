# Contributing to ID Protocol

Use synthetic profiles and examples. Never attach or commit real private context, credentials, chat exports, or third-party personal data.

## Set up and verify

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install ".[dev]" build twine
make validate
make drift-check
make coverage
make release-build
make release-check
```

A pull request should describe the behavior change, migration impact, and evidence. Add a regression test for policy, export, path-boundary, or compatibility changes. Keep package, schema, template, integration, and release-demo versions synchronized.

Protocol or compatibility proposals belong under `spec/RFC/`. Until v1.0.0, mark breaking changes clearly in the PR title and provide a migration path.
