---
name: learn-codebase
description: Teach an unfamiliar repository or code unit when the user requests onboarding, a learning path, architecture understanding, or a structured walkthrough. Do not trigger for a narrow factual code question, bug fix, or implementation unless learning is also requested.
---

# Learn a Codebase

## Boundaries

- Keep the target repository read-only unless changes are requested. Do not run installation, migration, deployment, or state-changing commands merely to understand it.
- Explain from inspected files and cite paths and symbols. Distinguish evidence from inferred design intent; do not expose secrets.
- Infer the learning goal and appropriate depth from the request. Ask only when ambiguity materially changes the explanation and cannot be resolved from the code.

## Select the Narrowest Mode

### Project Overview

Use for onboarding, architecture, or a reading route. Inspect applicable repository instructions, the primary README, manifests, entry points, and a representative feature path. Skip generated and vendored files unless central to the question.

Explain the project's purpose, major components, dependency direction, one runtime path, and useful files to read next. Include run commands, tests, or exercises only when useful to the learning goal; distinguish documented commands from commands actually executed.

For a deeper architectural survey, read only relevant sections of [references/inspection-guide.md](references/inspection-guide.md). Use [assets/learning-brief-template.md](assets/learning-brief-template.md) only when saving a study brief; omit irrelevant sections.

### Focused Walkthrough

Use for a requested walkthrough of a module, class, or function. Locate its definition and inspect surrounding imports, representative callers, state, or tests only as needed to explain it accurately. Do not require a full repository survey.

For a structured lesson, explain what it is, why it exists, and how one concrete scenario flows through it. For a narrow follow-up, answer that question directly without repeating the lesson structure. Do not invent author intent or paraphrase every line unless requested.

Read [references/focused-explanation-guide.md](references/focused-explanation-guide.md) only when complex lifecycle, control flow, or design motivation needs deeper treatment. Use [assets/code-unit-learning-template.md](assets/code-unit-learning-template.md) only when saving the explanation; adapt its sections to the requested depth.

Offer understanding checks or adjacent code only when the user wants interactive study. Preserve the established context on follow-up questions, and expand it only when new evidence requires it.
