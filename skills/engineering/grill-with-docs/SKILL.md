---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Run a `/grilling` session, using the `/domain-modeling` skill.

When the session ends, check for docs it wrote (`CONTEXT.md`, ADRs). If the user is continuing into `/to-spec`, leave them uncommitted — that skill commits the design artifacts on the spec's branch. Otherwise, offer to commit them before ending, so they don't dangle in the working tree.
