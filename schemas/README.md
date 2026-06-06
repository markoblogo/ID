# Schema Registry Index

This directory contains machine-readable schemas for `ID` artifacts and profile surfaces.

| Artifact | Version | Local path | Public `$id` |
| --- | --- | --- | --- |
| Interop context | v1 | `schemas/interop-v1.schema.json` | `https://raw.githubusercontent.com/markoblogo/ID/main/schemas/interop-v1.schema.json` |
| Compact context | v0 | `schemas/context-compact-v0.schema.json` | `https://raw.githubusercontent.com/markoblogo/ID/main/schemas/context-compact-v0.schema.json` |
| MCP resource | v1 | `schemas/mcp-context-resource-v1.schema.json` | `https://raw.githubusercontent.com/markoblogo/ID/main/schemas/mcp-context-resource-v1.schema.json` |
| Privacy policy | v1 | `schemas/privacy-policy-v1.schema.json` | `https://raw.githubusercontent.com/markoblogo/ID/main/schemas/privacy-policy-v1.schema.json` |
| Profile core | v1 | `schemas/profile-core.schema.json` | `https://raw.githubusercontent.com/markoblogo/ID/main/schemas/profile-core.schema.json` |
| Profile extended | v1 | `schemas/profile-extended.schema.json` | `https://raw.githubusercontent.com/markoblogo/ID/main/schemas/profile-extended.schema.json` |

Contracts used in scripts/CLI should reference local files directly while consuming
services should rely on the stable URL in `$id` for caching and reuse.
