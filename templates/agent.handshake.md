# AI Handshake (ID Protocol)

Use this message before any substantial task:

```
You are receiving Identity Context Package for this user.

Step 1: Confirm profile metadata (version, updated_at, trust_level).
Step 2: Summarize the user operating preferences in 5-10 bullets.
Step 3: List uncertain assumptions and ask clarifying questions only if critical.
Step 4: Commit to constraints from "Always do / Never do".
Step 5: Explain how output style will be adapted for this session.

If profile freshness is stale relative to freshness_ttl_days, warn explicitly and proceed with reduced confidence.
Do not invent user preferences that are not present.
```
