# Identity Diff

`idctl diff` shows what changed in an owner profile as semantic identity context, not just raw file hunks.

It supports the core positioning:

```text
git versions code
ID versions AI identity context
```

## Basic Use

Compare current working tree against `HEAD`:

```bash
idctl diff --owner-id <owner-id>
```

Compare against a previous time window:

```bash
idctl diff --owner-id <owner-id> --since 7d
```

Compare explicit refs:

```bash
idctl diff --owner-id <owner-id> --from v0.3.0 --to HEAD
```

Emit JSON:

```bash
idctl diff --owner-id <owner-id> --json
```

## What It Reports

`idctl diff` reads:
- `profile.minimal.md`
- `profile.core.md`
- `profile.extended.md`

It reports:
- changed profile files
- added, removed, and changed markdown sections
- semantic groups such as current goals, interaction contract, preferences, and domain focus
- stale profile metadata based on `updated_at` and `freshness_ttl_days`

Example:

```text
Identity Diff
Owner: markoblogo
Base: HEAD
Target: WORKTREE

Changed files:
- profiles/markoblogo/profile.core.md
  added: Current Goals
  changed: Communication Style

Semantic changes:
- current goals
  - profile.core.md: Current Goals
- interaction contract
  - profile.core.md: Communication Style

Stale assumptions: none
```

## Why It Exists

Raw diffs answer:

```text
which lines changed?
```

Identity Diff answers:

```text
what changed about how agents should work with this person?
```

That makes profile maintenance safer:
- new goals are visible
- communication contract changes are visible
- stale assumptions are visible
- profile drift becomes reviewable before generated artifacts are shared

## Current Scope

`idctl diff` is intentionally conservative in `v0.4.0`.

It does not claim to infer all memory contradictions or knowledge decay. It gives a stable audited base for those future checks:
- provenance-aware explanations
- candidate update review
- contradiction detection
- memory expiration
