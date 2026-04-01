---
profile_id: "markoblogo"
owner_alias: "markoblogo"
version: "0.1.1"
created_at: "2026-03-31"
updated_at: "2026-04-01"
freshness_ttl_days: 30
confidence_notes: "Черновик расширенного профиля; уточняется по реальным сессиям."
trust_level: "provisional"
---

# Extended Interaction Profile

## 1. Stable Preferences

- Working rhythm: итеративные короткие циклы с быстрым переходом к рабочему артефакту
- Decision style: сначала архитектурный каркас, затем прикладные операции
- Risk tolerance: готовность к экспериментам при сохранении контрольных точек

## 2. Domain Workflows

### Protocol / Repo Design

- Preferred output: спецификация + playbook + шаблоны + схемы
- Review checklist:
  - есть ли уровни контекста
  - есть ли handshake-контракт
  - есть ли правила актуализации

### Cross-AI Context Porting

- Preferred output: нейтральный профиль без привязки к одному вендору
- Constraints:
  - сохранять формулировки владельца там, где это критично
  - разделять подтвержденные и предположительные сведения

### Memory/Archive Systems

- Preferred output: индексируемые текстовые слои с provenance
- Constraints:
  - не выдумывать факты
  - отмечать неполные/сомнительные места

## 3. Recurrent Misalignments

- Модель меняется и теряется установленный стиль взаимодействия
- Редко используемые инструменты (например image/video) хуже понимают персональные ожидания
- Большой контекст без слоев перегружает старт сессии

## 4. Personal Lexicon

- "ID": протокол и репозиторий переносимого профиля взаимодействия человек ↔ ИИ
- "Use implies update": использование профиля требует обновления данных
- "Context depth": уровни L1/L2/L3 для разной глубины задач

## 5. Environment Assumptions

- Base path: `/Users/antonbiletskiy-volokh/Downloads/Projects/ID`
- VCS: Git + GitHub
- Privacy baseline: private-by-default для персональных данных

## 6. Decision Heuristics

- If task is short: использовать L1 + handshake
- If task is strategic: использовать L2 и журналировать изменения
- If historical depth is needed: подключать L3-источники с provenance

## 7. Known Good Prompts

- "Сначала дай краткое подтверждение понимания профиля и ограничений, затем выполняй задачу"
- "Не выдумывай личные предпочтения; если данных нет, явно пометь неопределенность"

## 8. Image/Video Generator Preferences

- Session bootstrap: сначала коротко подтверждать визуальный стиль, формат выдачи и ограничения перед генерацией.
- Prompt style: предпочитается структура "goal -> scene -> constraints -> output spec" без лишней художественной воды.
- Iteration mode: шаги мелкими итерациями (1-2 правки за цикл), с явным списком что именно изменилось.
- Consistency rule: при смене модели явно указывать риск стилевого дрейфа и предлагать адаптацию промпта.
- Output contract:
  - для изображений: указывать aspect ratio, style anchors, negative constraints;
  - для видео: указывать duration, shot list, tempo, transitions, final format.
