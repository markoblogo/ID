# ID Lite

## Goal

Get a usable personal context layer running with minimal setup cost.

Use `ID Lite` when you want:
- a fast bootstrap
- one maintained starter profile
- a compact portable context artifact
- a simple mental model

## Fast Path

### 1. Bootstrap

```bash
idctl init --owner-id <owner-id>
```

This creates:
- `profiles/<owner>/profile.minimal.md`
- `profiles/<owner>/handshake.md`
- `profiles/<owner>/privacy-policy.v1.json`

### 2. Fill the minimal profile

Edit:
- `profiles/<owner>/profile.minimal.md`

Only fill:
- communication style
- task rules
- quality bar
- priority domains
- short tool notes

### 3. Validate

```bash
make validate
```

### 4. Export the compact form

```bash
make compact
```

Use:
- `profiles/<owner>/context.compact.json`

## Best Use Cases

- onboarding a new coding agent
- moving your context between a few tools
- starting with one screen of maintained context instead of a full protocol workflow

## What You Are Not Doing Yet

`ID Lite` does not require:
- full extended profile work
- benchmark setup
- deep evidence maintenance
- broad ecosystem mapping

## Upgrade Path

When you outgrow Lite:
- move to `profile.core.md`
- add `profile.extended.md`
- adopt `ID Share` when external portability/privacy matters
- adopt `ID Bench` when you want measurable proof
