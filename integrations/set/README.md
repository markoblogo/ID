# ID 0.5.2 with SET 0.4.0 and agentsgen 0.5.0

ID owns reviewed human context. agentsgen owns repo instructions. SET orchestrates
both and exports bootstrap pointers. A pointer is not permission to read unrelated files.

## Local setup

Install `id-protocol==0.5.2`, create and review a profile, and refresh its soul.
Install `agentsgen==0.5.0` separately, then run in the target repository:

```sh
agentsgen init . --defaults --autodetect
agentsgen pack . --autodetect
idctl install-set-hook --path .
bash scripts/run_integration_hook.sh pre_task --owner-id demo --target set
```

The hook supports a minimal-only profile. It returns existing owner-local paths,
preferably soul, then core (or minimal), then handshake. Profile content is not
printed by the hook. Malformed or out-of-owner bootstrap paths are rejected.
Do not commit private source profiles to a public repository.

## GitHub Actions

Only use reviewed, appropriately scoped profiles in CI. The following steps assume
those files and the adapter are already available in the checked-out repository:

```yaml
- uses: actions/checkout@v7
- uses: actions/setup-python@v7
  with:
    python-version: '3.11'
- run: python -m pip install id-protocol==0.5.2
- uses: markoblogo/SET@v0.4.0
  with:
    workflow_preset: repo-docs
    id_enabled: 'true'
    id_pre_task: 'true'
    id_owner_id: demo
    id_target: set
```

SET produces `docs/ai/id-bootstrap.json` and `id-bootstrap.prompt.md` containing
pointers. Preserve or upload only artifacts approved for the workflow's audience.
Pin reviewed commit SHAs when immutable dependencies are required.

The ID release workflow tests the installed packages together and separately
runs this SET composite Action on synthetic fixture data.
