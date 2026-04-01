# ID Protocol Specification v0.1

## 1. Scope

ID Protocol defines a universal package that tells any AI tool how to communicate with a specific human.

Protocol unit: `Identity Context Package (ICP)`.

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

Any AI consuming profile must execute this sequence:

1. Confirm profile version and update date.
2. Summarize understanding in 5-10 bullets.
3. List assumptions and uncertainty.
4. Ask for correction if confidence is low.
5. Follow profile constraints in all outputs.

If profile is stale (`today - updated_at > freshness_ttl_days`), AI must warn about degradation risk.

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

## 7. Anti-Drift Rules

- never infer permanent preferences from one isolated prompt;
- separate stable traits from temporary state;
- track behavior corrections explicitly;
- keep quoted user instructions in original wording where possible.

## 8. Minimal Interop Format

Recommended human-readable source: Markdown.

Optional machine companion:
- JSON documents validated by provided schemas.

Recommended onboarding source:
- start from a minimal markdown profile, then grow into `profile.core.md` and `profile.extended.md` as evidence accumulates.

## 9. Non-Goals

- no claim of objective personality truth;
- no mandatory cloud sync;
- no replacement for private diaries or legal records.
