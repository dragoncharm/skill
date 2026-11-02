---
name: apply-iwhalecloud-dev-standards
description: Apply, explain, review, or maintain iWhaleCloud development standards when the user or repository requires 浩鲸/鲸云研发规范, including company-specific ZDubbo conventions. Use 公司规范 only when context identifies iWhaleCloud. Do not trigger for generic development, other companies, or non-engineering policies.
---

# Apply iWhaleCloud Development Standards

## Operating Principles

- Treat the bundled documents plus [references/incremental-standards.md](references/incremental-standards.md) as the source of truth for company-specific rules, with incremental rules taking precedence as the newest layer.
- Inspect the target project and its scoped instructions when assessing project applicability; answer standalone rule questions directly from the standards.
- Keep company code, configuration, customer data, credentials, and proprietary material local. Do not upload them to web services or quote more internal text than the task requires.
- Treat target projects as read-only for review or explanation requests. Modify them only when the user requests implementation or fixes.
- Separate confirmed company rules from general engineering advice. Never present an uncited best practice as an iWhaleCloud requirement.
- Apply applicable entries marked as user development preferences in [references/incremental-standards.md](references/incremental-standards.md) as default implementation choices. Keep their user-defined scope and exceptions; do not label them as formal company mandates or use them to bypass applicable mandatory requirements.
- Preserve unrelated user changes and existing project conventions unless a confirmed mandatory rule requires a scoped change.

## Workflow

### 1. Determine the Task and Scope

Route rule additions, amendments, and cancellations directly to Maintaining This Skill. For standalone rule explanations or citations, go directly to document selection without a project survey. For implementation, refactoring, compliance review, or project-specific design guidance, inspect enough files to determine:

- languages, frameworks, database engines, deployment domain, and runtime;
- whether the work is domestic or international when configuration or platform rules differ;
- repository-local instructions and documented tool versions;
- the changed or requested surface, including security and data boundaries.

Ask one focused question only when a domain choice would materially change the applicable rules and cannot be inferred safely.

### 2. Select the Applicable Documents

Use [references/catalog.md](references/catalog.md) to locate applicable documents when the route is not already known. Check applicable entries in [references/incremental-standards.md](references/incremental-standards.md) for newer overrides; reuse already-read entries unless changed. Search the smallest relevant subtree under `references/standards/` and read matching sections with their exceptions. Resolve resource paths relative to this `SKILL.md`.

Use `rg -n -i` with technology names, rule IDs, API names, and Chinese rule terms. For example:

```bash
rg -n -i '事务|连接|关闭|J000[0-9]+' references/standards/Java开发规范
rg -n -i '索引|分页|select|强制|禁止' references/standards/MySQL规范
```

Apply document status deliberately:

- Prefer an unmarked current document over a same-topic file marked `旧版-保留期`.
- Use `旧版-保留期` only for historical comparison or when the user explicitly targets the legacy version.
- Treat `公开评审` and `建设中` documents as provisional. Label every conclusion derived from them.
- Treat `暂缺` documents as coverage gaps, not as rules.
- Apply domestic, international, product-specific, language-specific, and database-specific documents only to their matching scope.
- Combine applicable security, red-line, language, framework, database, and delivery standards; do not assume one replaces another.

### 3. Extract Rules with Evidence

For every material decision, capture the document path, nearest heading, rule ID when present, and the document's exact strength term such as `强制`, `必须`, `严禁`, `禁止`, `推荐`, or `建议`.

Do not infer severity from wording when the document already labels it. If two applicable documents conflict:

1. prefer a user-added rule in `references/incremental-standards.md` over any bundled document;
2. prefer the current formal document over legacy or provisional material;
3. prefer the more specific matching scope over a general scope;
4. report any remaining conflict with both citations instead of silently choosing.

If no company rule covers the issue, state that clearly and label any subsequent recommendation as general engineering advice.

### 4. Perform the Requested Work

For implementation or refactoring:

- apply confirmed mandatory rules to the smallest coherent change;
- follow relevant security and red-line requirements even when the user mentions only a language standard;
- preserve the project's supported versions and APIs unless a cited rule requires migration;
- add or update tests when needed to verify changed behavior; reuse adequate existing coverage;
- avoid broad cleanup of pre-existing violations outside the requested scope.

For review or compliance checks:

- inspect concrete code or artifacts rather than returning a generic checklist;
- prioritize security red lines and mandatory violations, then recommendations;
- distinguish violations introduced by the reviewed change from pre-existing debt;
- provide a minimal remediation for every actionable finding.

For database, DevOps, configuration, delivery, or operations work:

- confirm the engine, environment, and domestic/international domain;
- select the matching design, development, operations, security, and delivery documents;
- do not execute deployments, migrations, releases, or production changes unless the user explicitly requests them.

### 5. Verify and Report

When implementation was requested, run checks appropriate to the changed behavior and project requirements. If another workflow coordinates the task, let it schedule verification and reuse its results for unchanged code, configuration, and environment. Rerun affected checks after relevant changes. Never claim a check passed unless it ran successfully.

Report:

1. the scope and standards consulted;
2. changes made or findings, ordered by rule strength and impact;
3. evidence as `document path — heading — rule ID/strength`, with line references when available;
4. verification performed;
5. provisional rules, coverage gaps, conflicts, or checks not run.

Keep citations concise. Paraphrase internal standards and quote only the minimum language needed to establish the requirement.

## Maintaining This Skill (Adding New Rules)

When the user supplies a new standard, rule, or team decision to incorporate — for example 把这条规范加进去 or 团队要求以后 XX 一律 YY — update this skill instead of only answering inline:

1. Clarify the rule until it is checkable against code: scope (languages, databases, domestic/international), strength (强制/推荐/...), and any exceptions. Ask one focused question only when the answer would change the rule's meaning.
2. Locate the source repository from the current workspace or known skill source. Prefer its skill directory as the edit target; if unavailable, report this and ask for the source location only when it cannot be inferred. Do not edit an installed copy as a fallback without an explicit request to update that copy. Append one entry to [references/incremental-standards.md](references/incremental-standards.md) in that file's documented format, resolving the write path relative to the selected source skill directory. Never edit the bundled documents under `references/standards/`.
3. To amend or cancel an existing incremental rule, add a superseding entry and mark the old entry superseded, as documented in that file. Do not rewrite or delete old entries.
4. Keep the source repository authoritative. Sync an installed copy only when the user explicitly requests that sync.
5. Validate the edited skill with `python3 /Users/Admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py` against the edited copy when that script is available.
6. Confirm to the user exactly which entry was added or changed, quoting the entry ID, and apply the new rule to the current task immediately.

Treat task-only rules as temporary. Persist rules only when the user requests adding or updating the standards; ambiguous permanence does not block applying a rule to the current task.

## Failure and Ambiguity Handling

- Stop and request sanitized input if the task cannot proceed without exposing credentials, customer data, or core confidential material to an external service.
- State that evidence is incomplete when a rule depends on an unavailable image attachment.
- Do not fill a `暂缺` topic from memory or from a neighboring database standard.
- Do not elevate a `公开评审` or `建设中` statement to formal policy.
- Do not use web search to replace or reinterpret the bundled internal standards. Use external official documentation when needed to verify public API or tool behavior without disclosing internal material; do not present it as company policy.
