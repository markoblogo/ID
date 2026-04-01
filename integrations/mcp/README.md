# MCP Wrapper Example

## Purpose

Show how `ID` compact context can be carried into an MCP-oriented wrapper without pretending that MCP itself defines profile semantics.

## Reference Payload

Use:
- `integrations/mcp/context.resource.example.json`

This example wraps:
- compact context fields
- explicit freshness and trust semantics
- loss notes

## Mapping Rule

- source of truth remains markdown profile files
- compact export is the short portable payload
- MCP wrapper carries that payload as structured resource data

## Conformance Claim

Suggested claim:

```text
Conformance: Level 2-3
Source: profile.core.md -> context.compact.json
Target: MCP resource payload
Known loss: extended workflows and historical context omitted
```
