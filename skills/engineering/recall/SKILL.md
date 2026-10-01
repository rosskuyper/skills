---
name: recall
description: Answer a bounded question from the spec archive via a low-cost worker. Use when the user or another skill asks why something was decided, what an earlier spec or ticket said, whether something was tried before, or needs anything from `docs/specs/` beyond the feature currently being worked.
---

# Recall

`docs/specs/` is the **spec archive**: every past spec, ticket, and wayfinder map. It is read only by a cheap worker. The caller stays out of it and works from the worker's short answer. `CONTEXT.md` and `docs/adr/` are the summary layer; read those directly.

## Input

One bounded question — "why did we choose X", "what did the billing spec decide about retries", "was Y attempted before". Add any hints you have: a feature slug, a date range, a term. Split a broad question into separate recalls.

## Delegate one worker

Spawn **one** worker on the cheap tier (Luna or Sonnet or equivalent), low effort, with conversation inheritance disabled where supported (for example, `fork_turns="none"`). Pass a bounded brief: the question, the hints, the search recipe, and the return contract below. Nothing else from the conversation.

Search recipe:

1. List `docs/specs/*/` by date; narrow by slug or date range when given.
2. Grep `docs/specs/`, `docs/adr/`, and `.out-of-scope/` for the terms and their `CONTEXT.md` synonyms.
3. Read only the matching sections of `spec.md`, `tickets/*.md`, `map.md`, ADRs, and out-of-scope notes.
4. For when or why questions, run `git log -S<term> --oneline` and `git log --grep=<term> --oneline`, then read only the commits that matter.

Return contract, at most 300 words:

- **Answer** — the direct answer, or "not found" with where it looked.
- **Confidence** — high, medium, or low, with the reason.
- **Pointers** — path plus heading for each source, for example `docs/specs/2026-10-01-billing-webhooks/spec.md` § Retries.
- **ADR coverage** — the ADR that already records it, or none.
- **ADR gap** — flag a decision that lives only in the archive yet meets the ADR gate: hard to reverse, surprising without context, and a real trade-off.

## Relay

Pass the answer and pointers on as returned. The worker's reading is the reading: re-check nothing in the archive yourself. On a low-confidence or not-found answer, say so and offer a sharper follow-up recall. On an ADR gap, tell the user they may run `/domain-modeling` to record it.

If subagents or model overrides are unavailable, say so and ask the user before reading the archive inline.

## Example brief

> Question: why do billing webhooks retry through a queue instead of inline? Hints: slug `billing-webhooks`, term `retry`. Search `docs/specs/*billing-webhooks*/` first, then grep `docs/specs/`, `docs/adr/`, and `.out-of-scope/` for `retry` and `outbox`; run `git log -S"retry queue" --oneline`. Read only matching sections. Return ≤300 words: answer, confidence with reason, pointers as path + heading, ADR coverage, and any ADR gap.
