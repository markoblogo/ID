# Public Benchmark Metrics

Runs analyzed: 4

## Public Utility Signals

- 2026-03-31 | baseline-2026-03-31-codex | codex | mode=id | success=0.9 alignment=88.7 latency=4.3 clarify=0.8 first_pass=0.3 prompt_avg_chars=281.6
- 2026-03-31 | control-2026-03-31-codex-no-id | codex | mode=no_id | success=0.3 alignment=68.7 latency=5.8 clarify=1.8 first_pass=0.0 prompt_avg_chars=889.6
- 2026-04-01 | baseline-2026-04-01-claude | claude-sonnet-4 | mode=id | success=0.9 alignment=85.3 latency=5.0 clarify=1.1 first_pass=0.3 prompt_avg_chars=301.6
- 2026-04-01 | control-2026-04-01-claude-no-id | claude-sonnet-4 | mode=no_id | success=0.3 alignment=68.7 latency=5.8 clarify=1.8 first_pass=0.0 prompt_avg_chars=907.6

## With vs Without ID Delta

- claude-2026-04-01 | with_id=baseline-2026-04-01-claude | without_id=control-2026-04-01-claude-no-id | success_delta=0.6 alignment_delta=16.6 latency_improvement=0.8 clarify_improvement=0.7
- codex-2026-03-31 | with_id=baseline-2026-03-31-codex | without_id=control-2026-03-31-codex-no-id | success_delta=0.6 alignment_delta=20.0 latency_improvement=1.5 clarify_improvement=1.0

Average deltas:
- onboarding_latency_min: 1.15
- clarification_turns_avg: 0.85
- task_success_rate: 0.6
- high_alignment_rate: 0.6
- first_pass_success_rate: 0.3
- alignment_index: 18.3

## Prompt Length Reduction

- average_reduction_ratio: 0.676
- average_reduction_chars: 607.0
- claude-2026-04-01 | with_id=baseline-2026-04-01-claude | without_id=control-2026-04-01-claude-no-id | avg_ratio=0.668 avg_chars=606.0
- codex-2026-03-31 | with_id=baseline-2026-03-31-codex | without_id=control-2026-03-31-codex-no-id | avg_ratio=0.683 avg_chars=608.0

## Profile Freshness

- owner: markoblogo
- overall_score: 0.0
- profiles/markoblogo/profile.core.md: score=0.0 age_days=74 ttl=14
- profiles/markoblogo/profile.extended.md: score=0.0 age_days=73 ttl=30

## Not Yet Instrumented

