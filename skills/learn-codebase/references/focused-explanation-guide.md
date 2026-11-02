# Focused Code Explanation Guide

Read this guide for deeper walkthroughs of complex lifecycle, control flow, or design motivation. Select only questions relevant to the target.

## Scope the Target

- Resolve the exact definition and distinguish same-named symbols.
- Identify the containing package, layer, or feature.
- Find construction, registration, export, or import sites.
- Find representative callers and direct collaborators.
- Find the closest tests that express observable behavior.
- Expand outward only until the target's role and execution path are clear.

## What It Is

Establish identity before implementation details:

- What single sentence best defines the target?
- Is it an entry point, coordinator, domain object, adapter, repository, utility, data model, policy, or framework integration?
- What behavior does its public surface promise?
- What does it own, and what does it delegate?
- Is it stateful? If so, who creates it and how long does it live?
- Which dependencies are essential versus incidental implementation details?
- Which callers rely on it?

State explicit non-responsibilities when they prevent a common misunderstanding.

## Why It Exists

Separate evidence-backed purpose from inferred motivation:

- Which project requirement or flow needs this target?
- Which concern does it isolate?
- Why is it located in this layer or package?
- Does it provide reuse, substitution, testability, state ownership, boundary translation, or orchestration?
- What coupling, duplication, or leakage would likely occur without it?
- What tradeoffs does the design introduce?

Use evidence in this order when available:

1. architecture documentation and explicit comments;
2. tests and public contracts;
3. callers, dependency direction, and neighboring types;
4. naming and conventional patterns.

Label motivation as **Confirmed**, **Inferred**, or **Unknown**. Never present a common design pattern as proof of the author's intention.

## How It Works

Use a concrete scenario rather than cataloging every member:

1. Start at a real caller, event, request, command, or test.
2. Show how control reaches the target.
3. Follow the primary path in execution order.
4. Track important data shapes and state changes.
5. Explain the decisions that change control flow.
6. Identify I/O, persistence, networking, logging, events, and other side effects.
7. Show how failures are represented, handled, or propagated.
8. Connect claims to a representative test.

Use short code excerpts only when syntax itself is important. Prefer file paths and symbol names over copying large sections.

## Adapt by Target Type

### Module or Package

Explain its boundary, exports, internal subcomponents, dependency direction, initialization, and the feature or capability it owns.

### Class

Explain its role, construction, lifetime, invariants, collaborators, public methods, state transitions, and substitution or inheritance behavior where present.

### Function or Method

Explain its contract, preconditions, main path, transformations, branches, errors, side effects, complexity where material, and callers.

### Data Type or Model

Explain the concept represented, field meanings, invariants, construction rules, serialization, ownership, mutation, and consumers.

## Teach for Retention

- Introduce no more surrounding concepts than the current explanation requires.
- Translate framework vocabulary into project-specific meaning.
- Use one compact analogy only when it clarifies rather than replaces the code model.
- End with a one-sentence mental model the learner can recall.
- When interactive study is requested, ask the learner to predict behavior or trace a variant.
- Recommend the next adjacent symbol that expands the same execution path.

