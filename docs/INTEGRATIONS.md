# Integrations: agents.md, LAB, SET

## 1. agents.md Integration

Goal: обеспечить стабильный старт взаимодействия с coding/chat агентами.

Contract:
- перед задачей подгружается `profiles/<owner>/profile.core.md`;
- затем отправляется `profiles/<owner>/handshake.md`;
- агент обязан подтвердить понимание ограничений до выполнения.

Minimal flow:
1. Load L1 profile.
2. Run handshake confirmation.
3. Execute task.
4. Suggest changelog update.

## 2. LAB Integration

Goal: тестировать варианты промптов, профилей и правил оркестрации.

Artifacts to track:
- experiment id;
- profile version used;
- model/tool used;
- mismatch notes;
- resulting profile corrections.

Recommendation:
- хранить результаты в отдельной папке `lab/` (будущий этап) и ссылаться на них из `profiles/<owner>/CHANGELOG.md`.

## 3. SET Orchestration Integration

Goal: автоматизировать дисциплину актуализации профиля.

Required checks in pipeline:
- freshness check for profile files;
- mandatory handshake step before long tasks;
- reminder to append changelog entry after profile-backed session.

Suggested policy:
- block non-critical long runs if profile is stale > 2x TTL;
- allow override with explicit "reduced-confidence" marker.

## 4. Unified Protocol Hooks

Common hooks across ecosystems:
- `pre_task`: load profile + run handshake;
- `post_task`: append change note;
- `weekly`: review stale sections and bump `updated_at`.
