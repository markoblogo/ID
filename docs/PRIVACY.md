# Privacy and Redaction Policy (MVP)

## 1. Scope

This policy defines how personal data should be handled in ID Protocol repositories.

Default mode: private-first.

## 2. Data Classes

### Class A: Direct identifiers (high risk)

- full legal names (if unnecessary for task)
- emails
- phone numbers
- exact home/work addresses
- government IDs, passport/tax numbers
- account handles and profile URLs when identity disclosure is not required

### Class B: Sensitive context (medium risk)

- precise geolocation trails
- personal finance details
- private family/health records
- full chat transcripts with third-party personal details

### Class C: Operational preferences (low risk)

- communication style preferences
- workflow constraints
- quality criteria
- tool usage habits

## 3. Storage Rules

- `data/raw/`: never publish to public repositories.
- `data/normalized/`: keep private unless redacted.
- `data/processed/redacted/`: safe-share candidate layer.

## 4. Redaction Rules (MVP)

Must mask in shareable text:
- email addresses -> `[REDACTED_EMAIL]`
- phone-like sequences -> `[REDACTED_PHONE]`
- URLs -> `[REDACTED_URL]`
- likely account handles (`@name`) -> `[REDACTED_HANDLE]`
- IPv4 addresses -> `[REDACTED_IP]`

Optional manual masking before publication:
- unique personal names
- exact dates tied to sensitive events
- location granularity below city-level

## 5. Safe-Share Package

Goal: publish profile behavior and protocol usage without disclosing raw personal traces.

Recommended contents:
- profile templates
- profile core/extended with sensitive details removed
- protocol/operations docs
- redacted excerpts only (if evidence snippets are required)

## 6. Verification Before Publish

Checklist:
- no files from `data/raw/` are staged
- no direct identifiers remain in exported redacted text
- README and docs do not contain accidental secrets

## 7. Incident Rule

If sensitive data is committed by mistake:
1. stop further distribution,
2. rotate exposed secrets (if any),
3. rewrite git history if needed,
4. document incident and mitigation.

## 8. Machine-Readable Policy Layer

Use `profiles/<owner>/privacy-policy.v1.json` as the machine-readable companion to this document.

Validation command:

```bash
python3 scripts/validate_privacy_policy.py --owner-id <owner-id>
```

This layer defines explicit `always_share`, `local_only`, and `task_class_scoped` rules for profile and data paths.

## 9. Threat Model Link

Privacy policy is only one part of the trust story.

For stale-profile risk, policy drift, lossy export, and benchmark overclaim boundaries, see:
- `docs/THREAT_MODEL.md`
