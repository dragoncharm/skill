# Repository Inspection Guide

Use the relevant sections after the initial survey. Do not apply every check mechanically.

## Instruction Priority

Honor applicable repository instructions. Consult the following sources only when they resolve a question in the selected learning scope:

- `AGENTS.md` and scoped variants
- `README*`, `CONTRIBUTING*`, and architecture documents
- workspace manifests and package-level documentation
- formatter, linter, compiler, and test configuration

State when documentation and implementation disagree.

## Ecosystem Signals

### JavaScript and TypeScript

Inspect `package.json`, lockfiles, workspace configuration, `tsconfig*`, framework configuration, scripts, and conventional entry files. Trace imports from the entry point through routing or composition into one feature.

### Python

Inspect `pyproject.toml`, lockfiles, package layout, console scripts, framework setup, configuration, and test fixtures. Identify whether imports follow a `src/` layout and where dependency injection or application construction occurs.

### Go

Inspect `go.mod`, `cmd/`, `internal/`, package boundaries, constructors, interfaces, and tests. Trace from a `main` package into the primary service or command path.

### Rust

Inspect `Cargo.toml`, workspace members, `src/main.rs` or `src/lib.rs`, modules, features, traits, error types, and integration tests.

### JVM

Inspect Gradle or Maven configuration, modules, application bootstrap, dependency injection, resources, profiles, and test source sets.

### Native or Systems Projects

Inspect build definitions, library or binary targets, public headers, platform abstraction, examples, and test harnesses. Separate generated build output from source.

## Architecture Questions

Answer only those supported by evidence:

- Where is the process started?
- Where are dependencies composed?
- How does input enter the system?
- Where is domain logic separated from transport or storage?
- Where is state owned and mutated?
- Which boundaries call external systems?
- How are errors represented and propagated?
- How are configuration and secrets supplied?
- Which tests best document intended behavior?

## Representative Trace

Choose a path that is central, understandable, and covered by tests when possible. A useful trace includes:

1. external trigger;
2. entry or adapter;
3. validation and translation;
4. orchestration;
5. domain operation;
6. persistence or external call;
7. returned result or emitted side effect;
8. corresponding test.

Name relevant symbols and file paths. Avoid describing a hypothetical path as implemented behavior.

## Learning Route Heuristics

- Prefer files that explain several downstream files.
- Prefer one complete vertical slice over many disconnected abstractions.
- Introduce framework internals only after showing project-level intent.
- Pair production code with its closest behavioral test.
- Delay utilities and edge-case handlers until the main flow is clear.
- Separate concepts the learner must understand now from useful later details.

## Evidence Labels

Use plain language to distinguish confidence:

- **Confirmed:** directly supported by inspected code or current documentation.
- **Inferred:** strongly suggested by structure or naming but not fully traced.
- **Unknown:** evidence is missing, conflicting, generated, or inaccessible.

