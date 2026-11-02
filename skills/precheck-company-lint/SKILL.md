---
name: precheck-company-lint
description: Run or reproduce company pipeline checks for Java and JavaScript, interpret company scan reports, and fix findings when requested. Use for company preflight checks or company-reported violations; ordinary ESLint/PMD commands and generic code review do not automatically trigger this workflow.
---

# Precheck Company Lint

## Select Scope and Authorization

- **Check or explain:** Run the requested checks or interpret supplied reports. Do not edit source or persist configuration merely because findings exist.
- **Fix:** Correct only findings in the user's or coordinating workflow's authorized scope. Report pre-existing debt separately unless its repair is requested.
- **Maintain precheck configuration:** Derive and persist rules only when the user requests maintaining or aligning local checks with company results.

Preserve explicit tool and file limits even when this skill is invoked directly. Java coverage includes PMD, NCSS/codesize, CPD, Checkstyle, and FindBugs/SpotBugs; JavaScript coverage uses ESLint. This skill provides no SQL scanner.

Match the company report format when a sample or configuration establishes it; otherwise keep the tool’s native XML/JSON format and say so. Report only actual tool results. Never claim parity with company checks without matching evidence for configuration, versions, and source revision. Keep source, credentials, and internal reports local; use only public rule names in external documentation queries.

## Locate and Run Applicable Checks

Detect only the languages, source roots, tools, and configurations required by the selected scope. Prefer project-provided commands when they meet the requested company checks.

Resolve configuration in this order: repository company config → existing `code-check-config/` → tool defaults. State the selected level and any limits to company parity. Read the matching sections of [references/check-tools.md](references/check-tools.md) only for tool detection, manual commands, missing tools, or report formats that are not already known.

Use [scripts/run_code_checks.sh](scripts/run_code_checks.sh) for a full supported company precheck. It runs all available checks for detected languages and replaces reports in its output directory. For a single tool, affected-check rerun, or narrower source scope, invoke that tool directly; do not use the full runner to expand the request.

For check-only requests, use a fresh temporary output directory outside the target project unless the user specifies a report destination. For authorized project report output, use `code-check-results/` or the requested directory, keeping supplied company reports separate. Run `scripts/run_code_checks.sh <project_dir> <output_dir>` with an explicit output directory.

Reuse valid compiled classes for FindBugs/SpotBugs. When compilation is needed, use the applicable project build within authorized local validation. Do not run builds that require unapproved production access or destructive effects. Report missing tools or blocked checks and continue independent checks; do not install dependencies without authorization.

## Fix and Verify

Read only the applicable tool's section of [references/fixing-findings.md](references/fixing-findings.md) when fixing findings. Preserve intended behavior and unrelated user changes. Routine fixes and necessary affected tests within the agreed scope do not require repeated confirmation. Ask only when resolving a finding requires an undecided contract, material scope expansion, or sensitive operation.

Let the coordinating workflow own verification when one exists. Batch related fixes, then compile and rerun affected checks as necessary. Reuse results for unchanged code, configuration, and environment. Confirm that authorized findings are resolved and no new violations were introduced; do not require a clean report for unrelated historical debt.

Report findings by tool, file, rule, and severity; include before/after counts when fixing, actual configurations, skipped checks, and unresolved items. Finish when the authorized work and necessary verification are complete or specific external blockers are documented.

## Maintain Company Check Configuration

For requested configuration alignment, read the gap-closing section of [references/fixing-findings.md](references/fixing-findings.md). Use [scripts/derive_company_config.py](scripts/derive_company_config.py) with `<project_dir> <result_file>...` to maintain `code-check-config/`. Inspect the supplied report and its source revision before deriving rules. Reproduce a finding before fixing it when feasible; compare remaining findings after repair, without expecting repaired findings to remain reproducible.

Do not treat rules observed in reports as the complete company ruleset. Review unmapped rules and inferred thresholds, and retain project-provided configuration precedence.
