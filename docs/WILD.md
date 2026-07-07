# Works In The Wild

`ID` is useful when one person moves between AI tools but wants one reviewed source of truth.

The profile stays in git. Each tool receives the richest artifact it can consume.

```text
profile.* + soul.md + context.compact.json
        |
        v
Claude Code / Cursor / Continue / ChatGPT / Gemini / OpenAI API
```

## Scenario 1: Claude Code to ChatGPT

Goal: keep task style, risk tolerance, and current goals stable while changing assistants.

1. Maintain the owner profile:

   ```bash
   idctl init --owner-id <owner-id>
   idctl refresh-soul --owner-id <owner-id>
   idctl export-compact --owner-id <owner-id>
   ```

2. Start Claude Code with:

   ```text
   profiles/<owner-id>/soul.md
   profiles/<owner-id>/handshake.md
   ```

3. Move the same session to ChatGPT with:

   ```text
   profiles/<owner-id>/context.compact.json
   ```

Expected result:
- Claude Code and ChatGPT use the same answer length, language, quality bar, and constraints.
- Any mismatch becomes a profile update candidate instead of a hidden memory difference.

## Scenario 2: Cursor to Continue to Claude Code

Goal: use one owner profile across coding tools.

```text
Cursor
  |
  v
Continue
  |
  v
Claude Code
```

Recommended artifacts:
- `profile.core.md` when the tool can read files directly
- `soul.md` when the tool needs a short bootstrap prompt
- `context.compact.json` when the tool expects structured context

Before switching tools:

```bash
idctl diff --owner-id <owner-id> --since 7d
idctl validate
```

This answers:
- what changed since the last work block
- whether the profile is stale
- whether generated artifacts still validate

## Scenario 3: API Agent Handoff

Goal: send the smallest useful identity bundle to an API-based agent.

```bash
idctl export-compact --owner-id <owner-id>
```

Use:

```text
profiles/<owner-id>/context.compact.json
```

This keeps the API payload smaller than the full profile while preserving:
- communication contract
- current goals and priorities
- trust and freshness metadata
- explicit loss boundaries

## Scenario 4: MCP-Aware Wrapper

Goal: let a wrapper expose profile context as a resource instead of pasted prompt text.

```bash
idctl export-mcp --owner-id <owner-id>
idctl validate-mcp --owner-id <owner-id>
```

Use:

```text
profiles/<owner-id>/mcp.context.resource.json
```

This is the right path when a host can request a resource and apply privacy/export policy before an agent sees it.

## Demo Script

Thirty-second demo:

1. Create a profile.
2. Run `idctl refresh-soul`.
3. Ask Claude Code to follow `soul.md`.
4. Ask ChatGPT or another assistant to follow `context.compact.json`.
5. Run `idctl diff --owner-id <owner-id> --since 7d`.

The point is not that every model behaves identically.

The point is that identity context becomes portable, reviewable, and diffable instead of trapped inside one product.
