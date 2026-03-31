# ID Operations Playbook v0.1

## 1. Lifecycle

1. `ingest`:
collect source data and normalize into text artifacts.

2. `profile-build`:
create/update L1 and L2 profiles.

3. `handshake`:
provide profile + handshake instruction to target AI.

4. `session-run`:
execute work under profile constraints.

5. `post-session-update`:
append changelog entry and bump profile metadata if needed.

## 2. Data Ingestion Sources

Allowed examples:
- AI exports (ChatGPT, Claude, Gemini, etc.);
- social posts;
- messenger archives;
- transcripts from audio/video;
- OCR/vision descriptions.

For each source, keep:
- `source_name`;
- `export_date`;
- `transform_steps`;
- `privacy_notes`.

## 3. Normalization Rules

- convert to UTF-8 text;
- keep original timestamps if available;
- keep source references for traceability;
- mark uncertain extraction with `[uncertain]`.

## 4. Session Handshake Template

Before task execution, ask AI to return:
- profile understanding summary;
- high-risk mismatch points;
- plan to adapt output style.

If mismatch is detected, update profile before long task.

## 5. Freshness Policy

Default thresholds:
- L1: 14 days;
- L2: 30 days;
- L3 index: 60 days.

When stale, AI may continue but must mark reduced confidence.

## 6. Changelog Entry Format

Required fields:
- `date`;
- `session_context`;
- `sections_used`;
- `changes_made`;
- `open_questions`;
- `next_review_date`.

## 7. Governance Roles

- `owner`:
final authority on preferences and corrections.

- `maintainer`:
can structure and rewrite for clarity without changing intent.

- `agent`:
may propose edits, cannot silently rewrite user constraints.

## 8. Quality Checks

Run before release of profile update:
- no contradictory hard constraints;
- metadata dates are valid;
- stale sections are labeled;
- at least one recent changelog entry exists if profile used in last 30 days.

## 9. Privacy Model

Recommended repo visibility: private.

When sharing externally, generate redacted package:
- remove personal identifiers unless needed;
- remove private contacts and location granularity;
- keep behavior instructions and workflow preferences.
