# Ecosystem Map

```mermaid
flowchart TD
    ID[ID]
    SET[SET]
    agentsgen[agentsmd]
    lab[lab.abvx]
    decisionMap[DecisionMap]

    ID -->|portable context| agentsgen
    ID -->|portable context| lab
    ID -->|portable context| SET
    SET -->|repo workflows| agentsmd
    agentsgen -->|repo docs + checks| SET
    lab -->|discovery + catalog| agentsgen
    lab -->|experiment + registry| SET
    SET -->|proof queues + registry hooks| decisionMap
```

This map keeps dependencies explicit:

- `ID` defines portable human context and trust/freshness semantics.
- `SET` is orchestration, scheduling, and repo control.
- `agentsgen` is repository surface/document generation for agents and hooks.
- `lab.abvx` is the discovery/catalog layer for ecosystem entry.
- `DecisionMap` is an optional decision strategy companion.
