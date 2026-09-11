# Quickstart

## Goal

From zero to first useful AI-ready profile in 5–10 minutes.

## 0. Choose your path

- `Lite`: just enough context to run one profile.
- `Share`: structured export for multiple tools.
- `Bench`: measurable claims and benchmarking.

Decision point:
- if you want quick starter and first utility, go `Lite`;
- if you need portable artifacts right away, go `Share`;
- if you need proof for a review, start with `Bench`.

## 1. Bootstrapping a new owner

```bash
idctl init --owner-id <owner-id>
```

Result:
- `profiles/<owner-id>/profile.minimal.md`
- `profiles/<owner-id>/handshake.md`
- `profiles/<owner-id>/privacy-policy.v1.json`

Interactive wizard (when you want shell prompts instead of flags):

```bash
idctl init --interactive
```

## 2. Fill profile in concrete outcomes

- `profiles/<owner-id>/profile.minimal.md`
  - owner goals and language preferences
  - task rules and quality bar
  - priority domains and tool notes
- `profiles/<owner-id>/handshake.md`
  - concise rules for applying the profile without a repeated preamble

## 3. Validate and generate first artifacts

```bash
idctl validate --owner-id <owner-id>
idctl export-compact --owner-id <owner-id>
```

Expected output:
- `profiles/<owner-id>/context.compact.json`
- validation summary in terminal

Check whether the profile is safe to carry into the next tool:

```bash
idctl diff --owner-id <owner-id> --since 7d
```

This reports changed sections, semantic groups, and stale profile metadata.

## 4. Scale to next path

- `Lite`: stop here if you just need AI-ready context.
- `Share`: add `profile.core.md`, then validate and export only the formats you need:
  - `idctl validate-privacy --owner-id <owner-id>`
  - `idctl export-interop --owner-id <owner-id>`
  - `idctl export-mcp --owner-id <owner-id>` for an external MCP adapter
- `Bench`: clone the repository and use its benchmark targets; they are maintainer tools rather than installed CLI commands.

## 5. First useful workflow

- open a task and start from:
  - owner profile
  - handshake
  - compact context artifact (when sharing with another tool)

This verifies the profile in real work instead of polishing docs only.

For concrete tool-handoff scenarios, see `docs/WILD.md`.
