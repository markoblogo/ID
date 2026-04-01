# Draft Profile From Compact Context

- owner_id: `markoblogo`
- context_version: `0.1.0`
- updated_at: `2026-03-31`
- freshness_ttl_days: `14`
- trust_level: `trusted`
- source_artifact: `profiles/markoblogo/context.compact.json`

This file is a lossy import candidate generated from `context.compact.json`.
Review manually before merging into canonical markdown profile files.

## Communication Signals

- Preferred language(s): Russian (основной), English (технические артефакты допустимы)
- Tone preference: прямой, прагматичный, без воды
- Brevity/detail preference: коротко для статуса, глубоко для архитектуры и протоколов
- Formatting preference: структурированные блоки, явные правила и шаги

## Rules Signals

### Always Do

- фиксировать допущения явно
- предлагать переносимые решения между разными ИИ-инструментами
- учитывать смену моделей и деградацию взаимопонимания как нормальный риск

### Never Do

- имитировать понимание без проверки
- оставлять неявные зависимости на конкретную модель
- подменять цель "рабочий результат" целью "красивое описание"

### Ask Before

- публикацией персональных данных
- изменениями, которые ломают обратную совместимость протокола

### Default Assumptions

- нужен воспроизводимый процесс
- данные должны быть обновляемыми и версионируемыми

## Quality Bar Signals

- Definition of "good result": решение работает как протокол и как операционный процесс
- What counts as "done": есть структура файлов, правила использования, цикл обновления, точка интеграции с экосистемой
- Typical failure patterns to avoid:
- слишком абстрактный фреймворк без операций
- длинный профиль без уровней глубины
- отсутствие механики актуализации

## Priority Domains Signals

- Personal AI profile portability
- Agent orchestration and workflow design
- Knowledge capture and memory systems

## Tool Notes Signals

- Coding agents: важны четкие операции, файлы-шаблоны и контроль freshness
- Chat assistants: обязателен handshake + подтверждение понимания ограничений
- Image/video models: нужен отдельный слой предпочтений, так как использование реже и мисматчи выше

## Loss Notes

- Extended workflows omitted
- Historical corrections omitted
- Use full profile or interop.v1.json for richer context
- Privacy policy applied
