# ID Protocol Specification v0.2

## 1. Scope

ID Protocol defines a universal package that tells any AI tool how to communicate with a specific human.

Protocol unit: `Identity Context Package (ICP)`.

Practical model:
- `profile.*` is source
- `soul.md` is a derived bootstrap artifact
- `context.compact.json` is a compact release bundle
- `idctl diff` is the semantic review surface

## 2. Package Levels

### L1: Core

Use for short sessions and default assistants.

Contains:
- communication style;
- task format preferences;
- hard constraints (`do / do not`);
- quality bar and review expectations;
- domain priorities.

Target size: 0.5-2 pages.

Practical onboarding note:
- a one-screen minimal profile is a valid starting point before a fuller L1 profile is written.

### L2: Extended

Use for longer sessions and specialized agents.

Contains:
- L1 + workflows by domain;
- recurrent mistakes to avoid;
- decision rules;
- personal glossary;
- known tools and environment assumptions.

Target size: 3-15 pages.

### L3: Full

Use for deep research and continuity over months/years.

Contains:
- L2 + linked artifacts:
- notes, wiki, posts, chat exports, transcripts, media-derived text;
- timeline and memory index;
- provenance metadata.

## 3. Mandatory Metadata

Each profile file must include:
- `profile_id`;
- `owner_alias`;
- `version`;
- `created_at` (ISO date);
- `updated_at` (ISO date);
- `freshness_ttl_days`;
- `confidence_notes`.

## 4. Handshake Contract

Any AI consuming a profile must:

1. Confirm profile version and update date.
2. Apply the relevant profile constraints without restating them by default.
3. Surface only assumptions or uncertainty that can change the result.
4. Ask for correction only when blocked or when confidence is too low to act safely.

If the profile is stale (`today - updated_at > freshness_ttl_days`) and freshness matters to the task, the AI must warn briefly about reduced confidence.

## 5. Trust Levels

### `trusted`

Data confirmed by owner and updated recently.

### `provisional`

Likely valid but not recently confirmed.

### `archival`

Historical context; may be outdated.

AI must prioritize: `trusted > provisional > archival`.

## 6. Update Economics

Rule: "Use implies update".

If a profile section was operationally used in a meaningful session, user or agent should append one entry to changelog:
- what was used;
- what changed;
- what remains uncertain.

Version bump and freshness rules for meaningful vs cosmetic changes are defined in:
- `docs/VERSIONING.md`

## 7. Anti-Drift Rules

- never infer permanent preferences from one isolated prompt;
- separate stable traits from temporary state;
- track behavior corrections explicitly;
- keep quoted user instructions in original wording where possible.

## 8. Minimal Interop Format

Recommended human-readable source: Markdown.

Optional machine companions:
- JSON documents validated by provided schemas;
- `privacy-policy.v1.json` for machine-readable trust/privacy rules.

Recommended onboarding source:
- start from a minimal markdown profile, then grow into `profile.core.md` and `profile.extended.md` as evidence accumulates.

## 9. Capability Negotiation

Consumers should request the richest artifact they can reliably handle.

Default order:

1. `mcp.context.resource.json` when the host supports policy-aware resources.
2. `context.compact.json` when structured compact context is supported.
3. `soul.md` when the host needs a short human-readable bootstrap.
4. `profile.minimal.md` when only plain prompt text is available.

Consumers must not silently claim support for layers they ignored. Report a lossy handoff only when it affects the task.

## 10. Non-Goals

- no claim of objective personality truth;
- no mandatory cloud sync;
- no replacement for private diaries or legal records.
