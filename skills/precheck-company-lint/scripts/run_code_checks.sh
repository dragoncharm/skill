#!/usr/bin/env bash
# Run company-style static code checks locally and produce one result file per check.
#
# Usage: run_code_checks.sh <project_dir> [output_dir]
#
# Checks attempted (only when the tool is available and the language applies):
#   Java: PMD, PMD codesize (NCSS-equivalent), CPD duplicate code, Checkstyle,
#         FindBugs/SpotBugs on compiled classes
#   JS:   ESLint
#
# Result files are written to <output_dir> (default: <project_dir>/code-check-results):
#   pmd-report.xml, ncss-report.xml, cpd-report.xml, checkstyle-report.xml,
#   findbugs-report.xml, eslint-report.json
#
# A check whose tool is missing is reported as SKIPPED, never silently ignored.
# Config precedence: repo-local company config first, then <project>/code-check-config/
# (self-maintained by derive_company_config.py from company result files), then
# tool defaults.
# Env overrides (executable paths only): PMD_CMD, CHECKSTYLE_CMD (may include
# "java -jar ..."), SPOTBUGS_HOME, FINDBUGS_HOME, CPD_MIN_TOKENS.

set -u

PROJECT_DIR="${1:?usage: run_code_checks.sh <project_dir> [output_dir]}"
OUTPUT_DIR="${2:-$PROJECT_DIR/code-check-results}"
CPD_MIN_TOKENS="${CPD_MIN_TOKENS:-}"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "ERROR: project dir not found: $PROJECT_DIR" >&2
  exit 2
fi
# Make both paths absolute: ESLint runs after `cd` into the project.
PROJECT_DIR=$(cd "$PROJECT_DIR" && pwd) || exit 2
mkdir -p "$OUTPUT_DIR" || exit 2
OUTPUT_DIR=$(cd "$OUTPUT_DIR" && pwd)
# Clear reports from a previous run so the summary only reflects this run.
for f in pmd-report.xml ncss-report.xml cpd-report.xml checkstyle-report.xml findbugs-report.xml eslint-report.json; do
  rm -f "$OUTPUT_DIR/$f"
done

RAN=0
SKIPPED=0

note()  { printf '%s\n' "$*"; }
skip()  { SKIPPED=$((SKIPPED + 1)); note "SKIPPED: $*"; }
ran()   { RAN=$((RAN + 1)); note "OK: $*"; }
fail()  { SKIPPED=$((SKIPPED + 1)); note "FAILED: $*"; }

# A check only counts as run when its report file exists and is non-empty;
# a zero exit code without a report means the invocation was wrong, not success.
report_ok() {
  if [ -s "$2" ]; then ran "$1 -> $2"; else fail "$1 produced no report at $2"; fi
}

# ---------------------------------------------------------------- sources ---

java_srcs=()
if [ -d "$PROJECT_DIR/src/main/java" ]; then
  java_srcs+=("$PROJECT_DIR/src/main/java")
else
  [ -d "$PROJECT_DIR/src" ] && java_srcs+=("$PROJECT_DIR/src")
fi
if [ "${#java_srcs[@]}" -eq 0 ] && command -v find >/dev/null 2>&1; then
  first_java=$(find "$PROJECT_DIR" -name '*.java' -not -path '*/target/*' -not -path '*/build/*' -print 2>/dev/null | head -1)
  [ -n "$first_java" ] && java_srcs+=("$(dirname "$first_java")")
fi

js_srcs=()
if [ -d "$PROJECT_DIR/src" ] && [ -n "$(find "$PROJECT_DIR/src" -name '*.js' -not -path '*/node_modules/*' -print 2>/dev/null | head -1)" ]; then
  js_srcs+=("$PROJECT_DIR/src")
fi

classes_dir=""
for d in target/classes build/classes/java/main; do
  [ -d "$PROJECT_DIR/$d" ] && classes_dir="$PROJECT_DIR/$d" && break
done

# Company config discovery: repo-local config first, then code-check-config/
# (derived from company result files), then tool defaults.
DERIVED_CFG_DIR="$PROJECT_DIR/code-check-config"

pmd_ruleset=$(find "$PROJECT_DIR" -maxdepth 3 -name 'pmd-ruleset.xml' -not -path '*/target/*' -not -path '*/node_modules/*' -not -path "$DERIVED_CFG_DIR*" -print 2>/dev/null | head -1)
if [ -z "$pmd_ruleset" ] && [ -f "$DERIVED_CFG_DIR/pmd-ruleset.xml" ]; then
  pmd_ruleset="$DERIVED_CFG_DIR/pmd-ruleset.xml"
fi

cs_config=$(find "$PROJECT_DIR" -maxdepth 3 \( -name 'checkstyle.xml' -o -name 'checkstyle-*.xml' \) -not -path '*/target/*' -not -path '*/node_modules/*' -not -path "$DERIVED_CFG_DIR*" -print 2>/dev/null | head -1)
[ -z "$cs_config" ] && cs_config=$(grep -l '<module name="Checker"' "$PROJECT_DIR"/*.xml 2>/dev/null | head -1)
if [ -z "$cs_config" ] && [ -f "$DERIVED_CFG_DIR/checkstyle.xml" ]; then
  cs_config="$DERIVED_CFG_DIR/checkstyle.xml"
fi

fb_include=""
[ -f "$DERIVED_CFG_DIR/findbugs-include.xml" ] && fb_include="$DERIVED_CFG_DIR/findbugs-include.xml"

if [ -z "$CPD_MIN_TOKENS" ] && [ -f "$DERIVED_CFG_DIR/config.json" ] && command -v python3 >/dev/null 2>&1; then
  CPD_MIN_TOKENS=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("cpd_min_tokens") or "")' "$DERIVED_CFG_DIR/config.json" 2>/dev/null)
fi
CPD_MIN_TOKENS="${CPD_MIN_TOKENS:-100}"

# ------------------------------------------------------------------ tools ---

resolve_pmd() {
  if [ -n "${PMD_CMD:-}" ] && command -v "$PMD_CMD" >/dev/null 2>&1; then echo "$PMD_CMD"; return 0; fi
  command -v pmd >/dev/null 2>&1 && echo pmd && return 0
  for p in "${PMD_HOME:-/nonexistent}/bin/pmd" "${PMD_HOME:-/nonexistent}/bin/pmd.sh"; do
    [ -x "$p" ] && echo "$p" && return 0
  done
  return 1
}

resolve_checkstyle() {
  if [ -n "${CHECKSTYLE_CMD:-}" ] && command -v "${CHECKSTYLE_CMD%% *}" >/dev/null 2>&1; then echo "$CHECKSTYLE_CMD"; return 0; fi
  command -v checkstyle >/dev/null 2>&1 && echo checkstyle && return 0
  jar=$(find "${CHECKSTYLE_HOME:-$PROJECT_DIR}" -maxdepth 2 -name 'checkstyle-*-all.jar' -print 2>/dev/null | head -1)
  [ -n "$jar" ] && echo "java -jar $jar" && return 0
  return 1
}

resolve_bugtool() {
  command -v spotbugs >/dev/null 2>&1 && echo spotbugs && return 0
  [ -x "${SPOTBUGS_HOME:-/nonexistent}/bin/spotbugs" ] && echo "${SPOTBUGS_HOME}/bin/spotbugs" && return 0
  command -v findbugs >/dev/null 2>&1 && echo findbugs && return 0
  [ -x "${FINDBUGS_HOME:-/nonexistent}/bin/findbugs" ] && echo "${FINDBUGS_HOME}/bin/findbugs" && return 0
  return 1
}

# ----------------------------------------------------------------- checks ---

if [ "${#java_srcs[@]}" -gt 0 ]; then
  java_csv=$(printf '%s,' "${java_srcs[@]}"); java_csv=${java_csv%,}
  note "== Java checks (sources: $java_csv) =="

  pmd=$(resolve_pmd)
  if [ -n "$pmd" ]; then
    rules="${pmd_ruleset:-category/java/errorprone.xml,category/java/bestpractices.xml}"
    # PMD 7: `pmd check -r <file>`; PMD 6: `pmd -reportfile <file>`.
    if "$pmd" check -d "$java_csv" -R "$rules" -f xml -r "$OUTPUT_DIR/pmd-report.xml" >/dev/null 2>&1 \
      || "$pmd" -d "$java_csv" -R "$rules" -f xml -reportfile "$OUTPUT_DIR/pmd-report.xml" >/dev/null 2>&1; then
      report_ok "PMD (rules: $rules)" "$OUTPUT_DIR/pmd-report.xml"
    else
      fail "PMD run (tried PMD 7 and PMD 6 syntax)"
    fi

    if "$pmd" check -d "$java_csv" -R category/java/codesize.xml -f xml -r "$OUTPUT_DIR/ncss-report.xml" >/dev/null 2>&1 \
      || "$pmd" -d "$java_csv" -R rulesets/java/codesize.xml -f xml -reportfile "$OUTPUT_DIR/ncss-report.xml" >/dev/null 2>&1; then
      report_ok "NCSS/codesize" "$OUTPUT_DIR/ncss-report.xml"
    else
      fail "NCSS/codesize run"
    fi

    if "$pmd" cpd --dir "$java_csv" --format xml --minimum-tokens "$CPD_MIN_TOKENS" > "$OUTPUT_DIR/cpd-report.xml" 2>/dev/null \
      || "$pmd" cpd --files "$java_csv" --format xml --minimum-tokens "$CPD_MIN_TOKENS" > "$OUTPUT_DIR/cpd-report.xml" 2>/dev/null; then
      report_ok "CPD duplicate code (min-tokens: $CPD_MIN_TOKENS)" "$OUTPUT_DIR/cpd-report.xml"
    else
      fail "CPD run"
    fi
  else
    skip "PMD/NCSS/CPD (pmd not installed; see references/check-tools.md)"
  fi

  cs=$(resolve_checkstyle)
  if [ -n "$cs" ]; then
    cfg="${cs_config:-/sun_checks.xml}"
    if $cs -c "$cfg" -f xml -o "$OUTPUT_DIR/checkstyle-report.xml" "${java_srcs[@]}" >/dev/null 2>&1; then
      report_ok "Checkstyle (config: $cfg)" "$OUTPUT_DIR/checkstyle-report.xml"
    else
      fail "Checkstyle run (config: $cfg)"
    fi
  else
    skip "Checkstyle (checkstyle or checkstyle-*-all.jar not found)"
  fi

  bugtool=$(resolve_bugtool)
  if [ -n "$bugtool" ]; then
    if [ -n "$classes_dir" ]; then
      fb_run() {
        if [ -n "$fb_include" ]; then
          "$bugtool" -textui -xml:withMessages -include "$fb_include" -output "$OUTPUT_DIR/findbugs-report.xml" "$classes_dir" >/dev/null 2>&1
        else
          "$bugtool" -textui -xml:withMessages -output "$OUTPUT_DIR/findbugs-report.xml" "$classes_dir" >/dev/null 2>&1
        fi
      }
      if fb_run; then
        report_ok "$(basename "$bugtool") (classes: $classes_dir${fb_include:+, include filter})" "$OUTPUT_DIR/findbugs-report.xml"
      else
        fail "FindBugs/SpotBugs run on $classes_dir"
      fi
    else
      skip "FindBugs/SpotBugs (no compiled classes under target/classes or build/classes/java/main; compile first)"
    fi
  else
    skip "FindBugs/SpotBugs (neither installed)"
  fi
else
  note "== No Java sources found; Java checks not applicable =="
fi

if [ "${#js_srcs[@]}" -gt 0 ]; then
  note "== JavaScript checks =="
  eslint_cmd="${ESLINT_CMD:-npx --no-install eslint}"
  if (cd "$PROJECT_DIR" && $eslint_cmd --version >/dev/null 2>&1); then
    if (cd "$PROJECT_DIR" && $eslint_cmd src --format json --output-file "$OUTPUT_DIR/eslint-report.json" >/dev/null 2>&1) \
      || (cd "$PROJECT_DIR" && $eslint_cmd . --format json --output-file "$OUTPUT_DIR/eslint-report.json" >/dev/null 2>&1); then
      report_ok "ESLint" "$OUTPUT_DIR/eslint-report.json"
    else
      fail "ESLint run (missing .eslintrc config?)"
    fi
  else
    skip "ESLint (not installed in project; npm i -D eslint)"
  fi
fi

# ---------------------------------------------------------------- summary ---

note ""
note "== Summary =="
count() { local n; n=$(grep -c "$2" "$1" 2>/dev/null); echo "${n:-0}"; }
[ -f "$OUTPUT_DIR/pmd-report.xml" ] && note "pmd-report.xml: $(count "$OUTPUT_DIR/pmd-report.xml" '<violation') violations"
[ -f "$OUTPUT_DIR/ncss-report.xml" ] && note "ncss-report.xml: $(count "$OUTPUT_DIR/ncss-report.xml" '<violation') violations"
[ -f "$OUTPUT_DIR/checkstyle-report.xml" ] && note "checkstyle-report.xml: $(count "$OUTPUT_DIR/checkstyle-report.xml" '<error ') violations"
[ -f "$OUTPUT_DIR/cpd-report.xml" ] && note "cpd-report.xml: $(count "$OUTPUT_DIR/cpd-report.xml" '<duplication') duplicate blocks"
[ -f "$OUTPUT_DIR/findbugs-report.xml" ] && note "findbugs-report.xml: $(count "$OUTPUT_DIR/findbugs-report.xml" '<BugInstance ') bug instances"
if [ -f "$OUTPUT_DIR/eslint-report.json" ]; then
  eslint_count=$(python3 -c '
import json,sys
try:
  data=json.load(open(sys.argv[1]))
  print(sum(len(f.get("messages",[])) for f in data))
except Exception:
  print("parse error")
' "$OUTPUT_DIR/eslint-report.json")
  note "eslint-report.json: $eslint_count messages"
fi
note "checks ran: $RAN, skipped/failed: $SKIPPED"

if [ "$RAN" -eq 0 ]; then
  note "RESULT: no check could run — install at least one tool (references/check-tools.md)."
  exit 1
fi
exit 0
