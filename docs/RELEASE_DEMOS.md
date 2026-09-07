# Reproducible release demos

Install ID 0.5.1, agentsgen 0.5.0, and abvx-set 0.3.1 in the same clean virtual
environment. From the ID source checkout, run:

```sh
python scripts/id_release_smoke.py --output docs/release-demo-results.json
```

The script creates temporary synthetic profiles and verifies:

1. Installed owner-only initialization, soul generation, compact/MCP exports and validation.
2. A synthetic private sentinel excluded from compact and MCP JSON by a local-only policy rule.
3. agentsgen's context manifest consumed by the installed ID hook and SET bootstrap exporter,
   with the original profile bytes unchanged and planning kept separate from applying.

[Recorded results](release-demo-results.json) report local wall-clock times.
No API calls or live AI sessions are involved; these are correctness demonstrations.
The full SET Action is tested separately in GitHub Actions.
