# Why ID

## Short Answer

`ID` makes human-AI working context:
- portable
- versioned
- privacy-aware
- measurable

That matters because most alternatives solve only one part of the problem.

## What It Beats

### Better than ad-hoc prompts

Ad-hoc prompts are easy to start with, but they degrade fast:
- copied by hand
- rewritten inconsistently
- hard to audit
- hard to compare across tools

`ID` turns stable guidance into maintained source files and generated transport artifacts.

### Better than chat-native memory alone

Chat-native memory is convenient, but usually:
- product-local
- hard to export
- hard to diff
- hard to validate

`ID` keeps the source of truth outside any one vendor product.

### Better than repo instructions alone

Repo instructions help for one codebase, but they do not generalize well to:
- writing
- research
- analysis
- multi-tool handoff

`ID` covers the person/tool interaction layer, not just the repo layer.

## What Makes It Different

`ID` is not only:
- a profile format
- a prompt template
- a benchmark pack
- a privacy note

It combines all of them into one protocol surface:
- markdown source of truth
- generated interop and compact artifacts
- privacy-policy layer
- benchmark and public metrics layer
- observed-behavior evidence

## What You Get

### 1. Faster onboarding

A new tool can start from:
- `profile.core.md`
- `context.compact.json`
- a handshake

instead of reconstructing preferences from scattered chat history.

### 2. Better portability

You can move between:
- chat tools
- coding agents
- local orchestrators
- MCP-style wrappers

without pretending every tool has the same memory model.

### 3. Stronger trust boundaries

`ID` makes freshness, trust, privacy, and loss visible.

That is better than hidden memory, silent drift, or undocumented context loss.

### 4. Measurable usefulness

This repo does not stop at “seems better”.

It tracks:
- onboarding latency
- clarification turns
- task success rate
- alignment index
- with-vs-without-ID deltas
- prompt length reduction

## Current Best Fit

`ID` is strongest today when you need:
- cross-tool continuity
- explicit privacy boundaries
- measurable workflow quality
- auditable generated artifacts

It is especially strong for:
- coding workflows
- protocol/research work
- structured writing/editorial workflows
- local agent orchestration

## Current Limits

`ID` does not eliminate:
- lossy exports
- vendor-specific behavior differences
- the need to maintain source profiles
- the need for human judgment on semantic changes

It is a protocol for disciplined portability, not magic memory.

## Bottom Line

If you want context that is:
- portable across tools
- explicit about trust and privacy
- benchmarkable
- reviewable in git

then `ID` is more durable than prompts, more portable than memory, and more auditable than one-tool instructions.
