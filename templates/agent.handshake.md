# AI Handshake (ID Protocol)

Use these rules when loading an ID profile:

```
You are receiving Identity Context Package for this user.

1. Verify profile metadata (version, updated_at, trust_level).
2. Apply relevant preferences and "Always do / Never do" constraints without repeating them.
3. Surface only uncertainty that can change the result; ask a question only when blocked.
4. Suggest a profile update when the owner corrects a stable preference or rule.

If profile freshness is stale relative to freshness_ttl_days and affects the task, warn briefly and proceed with reduced confidence.
Do not invent user preferences that are not present.
```
