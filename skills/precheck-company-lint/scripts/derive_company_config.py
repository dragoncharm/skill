#!/usr/bin/env python3
"""Derive local check configs from company check result files.

Usage: derive_company_config.py <project_dir> <result_file> [result_file ...]

Reads company result files in the tools' native formats (PMD XML, Checkstyle
XML, CPD XML, FindBugs/SpotBugs XML, ESLint JSON), extracts which rules the
company actually fired, and maintains a self-updating config directory:

  <project_dir>/code-check-config/
    observed-rules.json   source of truth: observed rules, counts, evidence
    pmd-ruleset.xml       PMD ruleset referencing the observed rules
    checkstyle.xml        Checkstyle config with the observed modules
    findbugs-include.xml  SpotBugs/FindBugs include filter (observed patterns)
    config.json           cpd_min_tokens estimate and evidence list

run_code_checks.sh picks this directory up automatically, so each round of
company results tightens the next local precheck.

Unrecognized file formats are reported and skipped, never guessed. PMD rules
that cannot be mapped to a category with confidence are listed as unmapped —
resolve them against the PMD docs and add the refs by hand; a wrong ref would
break the whole ruleset. Merging is idempotent: rerunning with the same files
changes nothing except the timestamp.
"""

import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from pathlib import Path

# PMD 7 category layout; only rules whose category is known with confidence
# are mapped — an unmapped guess would make PMD reject the ruleset.
PMD_RULE_CATEGORY = {
    "ExcessiveMethodLength": "codesize", "ExcessiveClassLength": "codesize",
    "ExcessiveParameterCount": "codesize", "CyclomaticComplexity": "codesize",
    "NPathComplexity": "codesize", "StdCyclomaticComplexity": "codesize",
    "ModifiedCyclomaticComplexity": "codesize", "TooManyMethods": "codesize",
    "TooManyFields": "codesize",
    "EmptyCatchBlock": "errorprone", "EmptyIfStatement": "errorprone",
    "EmptyWhileStmt": "errorprone", "EmptyTryBlock": "errorprone",
    "EmptyFinallyBlock": "errorprone", "BrokenNullCheck": "errorprone",
    "NullAssignment": "errorprone", "CompareObjectsWithEquals": "errorprone",
    "OverrideBothEqualsAndHashcode": "errorprone",
    "UselessOperationOnImmutable": "errorprone",
    "SystemPrintln": "bestpractices", "AvoidPrintStackTrace": "bestpractices",
    "UnusedImport": "bestpractices", "UnusedImports": "bestpractices",
    "CommentRequired": "documentation", "CommentSize": "documentation",
}

# Checkstyle modules that hang directly off Checker, not TreeWalker.
CHECKSTYLE_FILE_LEVEL = {
    "NewlineAtEndOfFile", "FileTabCharacter", "Header", "RegexpHeader",
    "RegexpSingleline", "RegexpMultiline", "JavadocPackage", "FileLength",
    "Translation", "UniqueProperties",
}

MIN_CPD_TOKENS_FLOOR = 50


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def sniff(path):
    text = path.read_text(errors="replace")
    stripped = text.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return "eslint", text
    if "<pmd-cpd" in text or "<duplication" in text:
        return "cpd", text
    if "<BugCollection" in text or "<BugInstance" in text:
        return "findbugs", text
    if "<checkstyle" in text:
        return "checkstyle", text
    if "<violation" in text or "<pmd " in text:
        return "pmd", text
    return None, text


def parse_pmd(text, found):
    for violation in ET.fromstring(text).iter("violation"):
        rule = violation.get("rule")
        if rule:
            found["pmd"][rule] += 1


def parse_checkstyle(text, found):
    for error in ET.fromstring(text).iter("error"):
        source = error.get("source", "")
        if not source:
            continue
        module = source.rsplit(".", 1)[-1]
        if module.endswith("Check"):
            module = module[: -len("Check")]
        if module:
            found["checkstyle"][module] += 1


def parse_cpd(text, found):
    for duplication in ET.fromstring(text).iter("duplication"):
        tokens = duplication.get("tokens")
        if tokens and tokens.isdigit():
            found["cpd_token_counts"].append(int(tokens))


def parse_findbugs(text, found):
    for bug in ET.fromstring(text).iter("BugInstance"):
        pattern = bug.get("type")
        if pattern:
            found["findbugs"][pattern] += 1


def parse_eslint(text, found):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    if not isinstance(data, list):
        return False
    for entry in data:
        for message in entry.get("messages", []):
            rule = message.get("ruleId")
            if rule:
                found["eslint"][rule] += 1
    return True


PARSERS = {
    "pmd": parse_pmd,
    "checkstyle": parse_checkstyle,
    "cpd": parse_cpd,
    "findbugs": parse_findbugs,
}


def load_observed(config_dir):
    path = config_dir / "observed-rules.json"
    if path.exists():
        try:
            data = json.loads(path.read_text())
            return data
        except (json.JSONDecodeError, OSError):
            print(f"WARNING: {path} unreadable, starting fresh")
    return {"pmd": {}, "checkstyle": {}, "findbugs": {}, "eslint": {},
            "cpd_min_tokens": None, "evidence": []}


def merge_counters(target, counter):
    for key, count in counter.items():
        target[key] = target.get(key, 0) + count


def write_pmd_ruleset(config_dir, pmd_rules):
    mapped = sorted(r for r in pmd_rules if r in PMD_RULE_CATEGORY)
    unmapped = sorted(r for r in pmd_rules if r not in PMD_RULE_CATEGORY)
    lines = [
        '<?xml version="1.0"?>',
        '<ruleset name="company-derived"',
        '    xmlns="http://pmd.sourceforge.net/ruleset/2.0.0"',
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '    xsi:schemaLocation="http://pmd.sourceforge.net/ruleset/2.0.0 '
        'https://pmd.sourceforge.io/ruleset_2_0_0.xsd">',
        '  <description>Derived from company check result files by '
        'derive_company_config.py. Category refs use PMD 7 layout.</description>',
    ]
    lines += [f'  <rule ref="category/java/{PMD_RULE_CATEGORY[r]}.xml/{r}"/>'
              for r in mapped]
    if unmapped:
        lines.append("  <!-- UNMAPPED rules seen in company results but not")
        lines.append("       confidently mapped to a category. Look each up in")
        lines.append("       the PMD docs and add a rule ref, or PMD will not")
        lines.append("       check them: -->")
        lines += [f"  <!-- {r} -->" for r in unmapped]
    lines.append("</ruleset>")
    (config_dir / "pmd-ruleset.xml").write_text("\n".join(lines) + "\n")
    return mapped, unmapped


def write_checkstyle_config(config_dir, modules):
    treeWalker = sorted(m for m in modules if m not in CHECKSTYLE_FILE_LEVEL)
    fileLevel = sorted(m for m in modules if m in CHECKSTYLE_FILE_LEVEL)
    lines = [
        '<?xml version="1.0"?>',
        '<!DOCTYPE module PUBLIC "-//Checkstyle//DTD Checkstyle Configuration '
        '1.3//EN" "https://checkstyle.org/dtds/configuration_1_3.dtd">',
        '<module name="Checker">',
        '  <property name="severity" value="warning"/>',
        '  <module name="TreeWalker">',
    ]
    lines += [f'    <module name="{m}"/>' for m in treeWalker]
    lines.append("  </module>")
    lines += [f'  <module name="{m}"/>' for m in fileLevel]
    lines.append("</module>")
    (config_dir / "checkstyle.xml").write_text("\n".join(lines) + "\n")


def write_findbugs_include(config_dir, patterns):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<FindBugsFilter>",
        "  <!-- Include filter: only patterns the company has actually fired.",
        "       Widens automatically as new company results are merged in. -->",
    ]
    lines += [f'  <Match><Bug pattern="{p}"/></Match>' for p in sorted(patterns)]
    lines.append("</FindBugsFilter>")
    (config_dir / "findbugs-include.xml").write_text("\n".join(lines) + "\n")


def main():
    if len(sys.argv) < 3:
        fail("usage: derive_company_config.py <project_dir> <result_file> ...")
    project_dir = Path(sys.argv[1]).resolve()
    if not project_dir.is_dir():
        fail(f"project dir not found: {project_dir}")
    config_dir = project_dir / "code-check-config"
    config_dir.mkdir(parents=True, exist_ok=True)
    observed = load_observed(config_dir)

    found = {"pmd": Counter(), "checkstyle": Counter(), "findbugs": Counter(),
             "eslint": Counter(), "cpd_token_counts": []}
    skipped, evidence = [], []

    for raw in sys.argv[2:]:
        path = Path(raw)
        if not path.is_file():
            skipped.append(f"{raw} (file not found)")
            continue
        if path.name in observed["evidence"]:
            # Same filename = same report; re-merging would double every count.
            skipped.append(f"{raw} (already merged; rename or clear "
                           "observed-rules.json to force re-merge)")
            continue
        kind, text = sniff(path)
        if kind in PARSERS:
            PARSERS[kind](text, found)
            evidence.append(path.name)
        elif kind == "eslint":
            if parse_eslint(text, found):
                evidence.append(path.name)
            else:
                skipped.append(f"{raw} (not an ESLint JSON report)")
        else:
            skipped.append(
                f"{raw} (unrecognized format — if it is a company-wrapped "
                "file, extract the rules manually and rerun)")

    for tool in ("pmd", "checkstyle", "findbugs", "eslint"):
        merge_counters(observed[tool], found[tool])
    observed["evidence"] = sorted(set(observed["evidence"]) | set(evidence))

    cpd_estimate = None
    if found["cpd_token_counts"]:
        # A reported duplicate proves the company threshold is <= its token
        # count, so the smallest reported block is the best estimate.
        estimate = max(min(found["cpd_token_counts"]), MIN_CPD_TOKENS_FLOOR)
        current = observed.get("cpd_min_tokens")
        cpd_estimate = min(current, estimate) if current else estimate
        observed["cpd_min_tokens"] = cpd_estimate

    observed["updated_at"] = datetime.now().isoformat(timespec="seconds")
    (config_dir / "observed-rules.json").write_text(
        json.dumps(observed, indent=2, ensure_ascii=False) + "\n")
    (config_dir / "config.json").write_text(json.dumps(
        {"cpd_min_tokens": observed["cpd_min_tokens"],
         "evidence": observed["evidence"],
         "updated_at": observed["updated_at"]},
        indent=2) + "\n")

    summary = [f"== Derived config in {config_dir} =="]
    if observed["pmd"]:
        mapped, unmapped = write_pmd_ruleset(config_dir, observed["pmd"])
        summary.append(f"pmd-ruleset.xml: {len(mapped)} rules mapped"
                       + (f", {len(unmapped)} UNMAPPED (see file comments): "
                          + ", ".join(unmapped) if unmapped else ""))
    if observed["checkstyle"]:
        write_checkstyle_config(config_dir, observed["checkstyle"])
        summary.append(f"checkstyle.xml: {len(observed['checkstyle'])} modules")
    if observed["findbugs"]:
        write_findbugs_include(config_dir, observed["findbugs"])
        summary.append(f"findbugs-include.xml: {len(observed['findbugs'])} patterns")
    if observed["eslint"]:
        summary.append("eslint rules observed (record only — config is manual, "
                       "plugins/parser unknown): " + ", ".join(sorted(observed["eslint"])))
    if observed["cpd_min_tokens"]:
        summary.append(f"cpd_min_tokens estimate: {observed['cpd_min_tokens']}")
    if not any((observed["pmd"], observed["checkstyle"], observed["findbugs"],
                observed["eslint"], observed["cpd_min_tokens"])):
        summary.append("nothing derived yet — pass result files to populate")
    for entry in skipped:
        summary.append(f"SKIPPED: {entry}")
    summary.append("run_code_checks.sh now picks this directory up automatically.")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
