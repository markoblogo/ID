# Why ID

AI tools remember context in different ways. Moving to another client or repository often means copying prompts, rebuilding preferences, and trusting context you cannot inspect.

ID keeps durable working context in owner-controlled files. You review the source, see semantic changes in git, and export only fields allowed by a per-profile privacy policy.

## When it helps

Use ID when you need one or more of these:

- the same working preferences across several AI tools;
- a reviewable boundary between personal context and repository instructions;
- compact, policy-filtered handoffs to agentsgen, SET, or a custom adapter;
- explicit freshness and trust metadata;
- reproducible checks for generated context artifacts.

For a single short-lived prompt, ID may add more structure than you need. It also cannot make different AI clients interpret context identically, and the owner must keep canonical profiles current.

## Where it sits

| Layer | Owner | Example |
| --- | --- | --- |
| Human context | ID | communication preferences, constraints, privacy policy |
| Repository context | agentsgen | `AGENTS.md`, commands, architecture pointers |
| Workflow orchestration | SET | review-first plans, hooks, exports |
| Client adapter | external tool | MCP resource, prompt, or client-specific import |

ID remains useful without the other tools. Its Markdown profiles are the source of truth; JSON files are generated transport views.

## What can be verified

The repository tests profile validation, policy-filtered omission, legacy-policy compatibility, semantic diffs, and installed-package handoffs. These checks demonstrate data handling and interoperability. They do not prove that an AI answer will be better in every client.

Start with the [five-minute quickstart](QUICKSTART.md) or inspect the [three release demos](RELEASE_DEMOS.md).
