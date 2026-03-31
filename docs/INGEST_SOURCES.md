# Ingest Sources and Normalization (MVP)

This document defines priority-1 ingestion for ID Protocol.

## 1. Goal

Convert heterogeneous exports into normalized text that can be used to draft and refine user interaction profiles.

## 2. Source Priority (Phase 1)

1. Chat exports:
- ChatGPT export
- Claude export
- Gemini export (if available)

2. Messenger/social text:
- Telegram export
- Facebook export
- Instagram export

3. Optional in phase 1:
- notes and docs archives
- transcript text from audio/video pipelines

## 3. Storage Contract

Raw files (immutable):
- `data/raw/<source>/...`

Normalized files (editable and deduplicated):
- `data/normalized/<source>/...`

Processed artifacts:
- `data/processed/...`

## 4. Minimum Source Metadata

For each source folder, create `SOURCE.md` with:
- `source_name`
- `export_date` (YYYY-MM-DD)
- `time_range`
- `transform_steps`
- `privacy_notes`

## 5. Normalization Rules (MVP)

- UTF-8 only.
- Keep timestamps when available.
- Preserve direct user wording for instructions/preferences.
- Mark uncertain extraction fragments with `[uncertain]`.
- Remove obvious binary/noise payloads from normalized layer.

## 6. Extractor Input Contract

`extract_profile.py` reads:
- `.txt`, `.md`, `.json` under `data/normalized/`

Expected content style:
- conversational text
- notes
- exported records where user statements are still present in text form

## 7. Extractor Output Contract

Main output:
- `profiles/<owner-id>/draft.from-exports.md`

Support output:
- `profiles/<owner-id>/conflicts.from-exports.md`

The draft is a candidate profile and requires owner review before promotion to `profile.core.md` or `profile.extended.md`.

## 8. Privacy Baseline

- Keep repository private when personal exports are present.
- Do not commit raw personal archives to public repositories.
- Prefer committing only normalized/redacted fragments for collaboration.

## 9. First Operational Run

1. Put exports into `data/raw/<source>/`.
2. Normalize into `data/normalized/<source>/`.
3. Run:
   - `python3 scripts/extract_profile.py --owner-id markoblogo`
4. Review generated draft and conflicts.
5. Manually merge approved findings into profile files.
