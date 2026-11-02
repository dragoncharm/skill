# Check Tools, Commands, and Result Formats

Use this reference to detect tooling, run each check manually, and parse result files.

## Tool Detection and Installation

| Check | Tool | Detect with | Install |
|---|---|---|---|
| PMD | PMD 6/7 | `command -v pmd` or `$PMD_HOME/bin/pmd(.sh/.bat)` | github.com/pmd/pmd/releases (zip; set `PMD_HOME`) |
| NCSS | PMD codesize/legacy ncss rules (or JavaNCSS) | same as PMD; `command -v javancss` optional | bundled with PMD |
| Duplicate code | PMD CPD | same as PMD | bundled with PMD |
| Checkstyle | Checkstyle 8/10 | `command -v checkstyle` or a `checkstyle-*-all.jar` | github.com/checkstyle/checkstyle/releases |
| FindBugs 3.0 | FindBugs (Java ≤8) or SpotBugs | `command -v findbugs` / `command -v spotbugs`, or `$FINDBUGS_HOME` / `$SPOTBUGS_HOME` | github.com/spotbugs/spotbugs/releases |
| ESLint | ESLint via npx | `npx --no-install eslint --version` in the JS project | `npm i -D eslint` |

Every check tolerates a missing tool: report `SKIPPED (<tool> not installed)` and continue with the rest.

## Company Config Discovery

Resolve config in this order — `run_code_checks.sh` applies the same order:

1. Repo-provided company config (checked into the target repo).
2. `<project>/code-check-config/` — derived and self-maintained by `scripts/derive_company_config.py` from past company result files (`pmd-ruleset.xml`, `checkstyle.xml`, `findbugs-include.xml`, `config.json` with the CPD token estimate; `observed-rules.json` is the source of truth).
3. Tool defaults.

What to look for at level 1:

If nothing is found, use the tool defaults and state clearly that the local config may differ from the company's.

## Commands

PMD 7 syntax (PMD 6 uses `pmd -d <src> -R <rules> -f xml -reportfile <out>`; try 7 first, fall back on failure):

```bash
pmd check -d <java-src> -R <ruleset-or-builtin> -f xml -r pmd-report.xml
```

NCSS/codesize variant — same command with the codesize ruleset, written to a separate file so it mirrors the company's separate NCSS report:

```bash
pmd check -d <java-src> -R category/java/codesize.xml -f xml -r ncss-report.xml
```

CPD duplicate code (token threshold 100 is the common company default; output goes to stdout):

```bash
pmd cpd --dir <java-src> --format xml --minimum-tokens 100 > cpd-report.xml
```

Checkstyle (needs a config; `-j` optional for parallel):

```bash
java -jar checkstyle-X-all.jar -c checkstyle.xml -f xml -o checkstyle-report.xml <java-src>
```

FindBugs 3.0 / SpotBugs (requires compiled classes; compile first with `mvn compile` or `gradle classes`):

```bash
findbugs -textui -xml:withMessages -output findbugs-report.xml <project>   # project dir or classpath
spotbugs  -textui -xml:withMessages -output findbugs-report.xml <project>
```

FindBugs 3.0 stops at Java 8 bytecode. For Java 9+ use SpotBugs (successor, reads the same filters and produces a compatible XML). Say which one ran and why.

ESLint (run inside the JS project so local config and dependencies resolve):

```bash
npx --no-install eslint "src/**/*.js" --format json --output-file eslint-report.json
```

## Result File Formats

- PMD XML: `<file name="...">` elements each containing `<violation beginline begincolumn rule priority>`; priority 1 = highest.
- CPD XML: one `<duplication lines tokens>` per duplicate block with `<file line>` children and a `<codefragment>`; group fixes per duplication.
- Checkstyle XML: `<file name="...">` with `<error line column severity message source>`; `source` ends in the rule id.
- FindBugs/SpotBugs XML: `<BugInstance type priority rank>` with `<SourceLine classname startLine>`; rank ≤ 9 is serious.
- ESLint JSON: array of `{ filePath, messages: [{ line, ruleId, severity, message }] }`; severity 2 = error.

When the user provides a company result file, inspect it to learn the exact format first — company platforms sometimes wrap or trim these XMLs — then map each entry back to the tool's native report so fixes can be verified by re-running the same local check.
