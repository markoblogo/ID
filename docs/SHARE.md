# ID Share

## Goal

Move context between tools or people without treating privacy and loss as afterthoughts.

Use `ID Share` when you want:
- a portable artifact
- explicit privacy policy
- documented loss boundaries
- safe-share discipline

## Core Pieces

- `profiles/<owner>/privacy-policy.v1.json`
- `profiles/<owner>/interop.v1.json`
- `profiles/<owner>/context.compact.json`
- `profiles/<owner>/mcp.context.resource.json`

Use one bootstrap command first:

```bash
idctl init --owner-id <owner-id>
```

## Typical Flow

### 1. Validate privacy policy

```bash
idctl validate-privacy --owner-id <owner-id>
```

### 2. Export portable artifacts

```bash
idctl export-interop --owner-id <owner-id>
idctl export-compact --owner-id <owner-id>
idctl export-mcp --owner-id <owner-id>
```

### 3. Choose the right share surface

- `interop.v1.json`
  - richest structured portable artifact
- `context.compact.json`
  - smallest practical portable context block
- `mcp.context.resource.json`
  - policy-aware transport wrapper for MCP-style workflows

### 4. Use safe-share / redaction when needed

```bash
idctl redact --input-dir <input-dir> --output-dir <output-dir> --report <report.json>
```

## Best Use Cases

- moving your context into another AI tool
- sharing a bounded portable profile with a collaborator
- passing context into a local orchestrator or MCP-style wrapper

## What Makes It Different

`ID Share` is not “export and hope”.

It keeps:
- source markdown canonical
- privacy policy explicit
- loss boundaries documented
- generated artifacts validated

## Upgrade Path

If you need proof that the profile actually helps:
- move to `ID Bench`
