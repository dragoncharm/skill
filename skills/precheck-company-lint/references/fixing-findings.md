# Fixing Findings and Closing Gaps

Fix strategies per check, verification steps, and the gap-closing workflow for company results the local run missed.

## Fix Principles

- Follow the repair scope and authorization in SKILL.md. Preserve intended behavior; ask only for undecided contracts, material scope changes, or sensitive actions.
- Batch related fixes within the authorized files; verify affected checks using the shared verification policy in SKILL.md.
- Exclude generated and third-party code via the tool's filter, not by editing it. Typical excludes: `target/`, `build/`, `node_modules/`, `**/gen/**`, `**/generated/**`.
- Match the surrounding style — naming, brace placement, import order — so the fix itself introduces no new Checkstyle/ESLint findings.

## Per-Check Fix Strategies

### PMD (general)

- `UnusedLocalVariable`, `UnusedPrivateMethod/Field`: delete after confirming no reflection or serialization references.
- `DataflowAnomalyAnalysis` style rules: rename or initialize rather than reorder logic.
- `EmptyCatchBlock`: either handle the exception, log it, or add a comment explaining why it is ignored — never leave it empty silently.

### NCSS / codesize

- `ExcessiveMethodLength` / high NCSS method count: extract cohesive steps into private methods with intent-revealing names; keep parameters small by passing the state the block needs.
- `ExcessiveClassLength`: split responsibilities into collaborators, starting with the largest cohesive private-method clusters.
- `CyclomaticComplexity` / `NPathComplexity`: replace nested if/else chains with early returns, guard clauses, or a lookup structure.
- `ExcessiveParameterCount`: introduce a parameter object only when the call sites allow it without churn.

### CPD duplicate code

- Duplicates inside one class: extract a private helper.
- Duplicates across classes: extract to a shared utility or base class the project already has; do not create a parallel util home.
- Near-duplicates that differ in constants: parameterize, but stop short of merging blocks whose behavior genuinely differs.
- Minimum token threshold matters: if the company reports duplicates below the local threshold, lower `--minimum-tokens` to match before claiming a fix is complete.

### Checkstyle

- Naming, import order/unused imports, whitespace, missing final, line length: mechanical fixes; batch them with the editor or a sed pass, then review the diff.
- Missing Javadoc: write a one-line summary that states what the member does, not a restatement of its name.
- Magic numbers: promote to named constants only when the value has meaning beyond the literal.

### FindBugs / SpotBugs

- `NP_DEREFERENCE_OF_NULL` / null-related: add a null guard or `Objects.requireNonNull` at the boundary where null enters, not at every use site.
- `OS_OPEN_STREAM`, `OBL_UNSATISFIED` (resource leaks): switch to try-with-resources.
- `EI_EXPOSE_REP` / `EI_EXPOSE_REP2`: defensive copy at construction and accessor, or document why exposure is intentional if the class is effectively immutable/throwaway.
- `SE_BAD_FIELD` and serialization issues: fix only with the user when the wire format could change; otherwise document.
- `DM_STRING_CTOR`, `SIC_INNER_SHOULD_BE_STATIC` and similar performance smells: safe mechanical fixes.

### ESLint

- When fixes are authorized, use the project ESLint command with `--fix` limited to the authorized files for mechanical fixes; inspect its diff before handling the remainder.
- `no-unused-vars`: prefix intentional discards per the project's convention (`_name`) or remove.
- Complexity/function-size rules: same extraction approach as NCSS.

## Gap-Closing Workflow (company findings the local run missed)

1. Only when configuration alignment is requested, inspect the report and source revision, then run `scripts/derive_company_config.py <project_dir> <result_file>...`. It merges every rule, module, and bug pattern the company fired into `<project>/code-check-config/` (`observed-rules.json` is the source of truth; the XML files are regenerated from it), so the knowledge survives the session and `run_code_checks.sh` uses it on the next run.
2. Review the derivation output: resolve UNMAPPED PMD rules via the PMD docs and add refs to `code-check-config/pmd-ruleset.xml`; note that ESLint rules are record-only (config must be written by hand — a report cannot reveal parser or plugin needs).
3. Parse the company result file and list the violations the local run did not reproduce.
4. For each, determine the cause:
   - **Rule absent locally** → it should now be covered by the derived config; if not, add it by hand, matching the company's severity.
   - **Different tool version** → note the version difference; prefer aligning the local tool version if practical, otherwise compensate with an equivalent rule.
   - **Different threshold** (CPD tokens, NCSS limits, complexity caps) → the CPD estimate in `code-check-config/config.json` is the smallest reported duplicate's token count; copy exact thresholds into the config once known.
   - **Stale or different source** → verify the line numbers against the current source; if the company ran on an older revision, say so instead of "fixing" already-changed code.
5. Reproduce findings with the aligned checks before repair when feasible. Fix violations only when repair is authorized, using the strategies above.
6. Rerun affected checks after repair; run the full precheck only if configuration changes affect the full set. Compare resolved and remaining findings against the baseline. Do not require repaired violations to reproduce or unrelated historical debt to reach zero.
7. Report what remains unmatched and why — some company platforms run proprietary extra checks with no public rule equivalent; be explicit rather than pretending parity.
