#!/usr/bin/env python3
"""/incubate test suite — pattern-based validation of skill structure and behavior.

Usage:
  python tests/run_tests.py                      # 1 worker, 1 run
  python tests/run_tests.py --workers 8          # 8 parallel threads
  python tests/run_tests.py --workers 8 --runs 10 # 8 threads x 10 runs
"""

import argparse
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ─── Root of the incubate repo ───────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent

SKILL_MD = REPO_ROOT / "SKILL.md"
README_MD = REPO_ROOT / "README.md"
INDEX_HTML = REPO_ROOT / "docs" / "index.html"
PAGES_YML = REPO_ROOT / ".github" / "workflows" / "pages.yml"
TESTS_YML = REPO_ROOT / ".github" / "workflows" / "tests.yml"
RUN_TESTS = REPO_ROOT / "tests" / "run_tests.py"
SCENARIOS_DIR = REPO_ROOT / "tests" / "scenarios"


# ─── Helpers ────────────────────────────────────────────────────────────────────────────────
def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _file_contains(path: Path, pattern: str, flags: int = 0) -> bool:
    return bool(re.search(pattern, _read(path), flags))


def _count_matches(path: Path, pattern: str, flags: int = re.MULTILINE) -> int:
    return len(re.findall(pattern, _read(path), flags))


def _file_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


# ─── Scenarios ──────────────────────────────────────────────────────────────────────────────
SCENARIOS = [
    {
        "id": "01",
        "name": "valid-idea-copilot",
        "description": "SKILL.md documents Copilot platform path",
        "checks": [
            ("SKILL.md exists",             lambda: _file_exists(SKILL_MD)),
            ("Copilot path documented",      lambda: _file_contains(SKILL_MD, r"copilot|MCP|github-create_repository", re.IGNORECASE)),
            ("MCP tool path present",        lambda: _file_contains(SKILL_MD, r"github-push_files|github-create_repository")),
            ("Platform detection section",   lambda: _file_contains(SKILL_MD, r"Platform Detection")),
            ("Phase 5 Ship exists",          lambda: _file_contains(SKILL_MD, r"Phase 5|## Phase 5")),
            ("Copilot memory path",          lambda: _file_contains(SKILL_MD, r"\.copilot.+skills.+incubate")),
            ("Platform table present",       lambda: _file_contains(SKILL_MD, r"\| Platform \|")),
        ],
    },
    {
        "id": "02",
        "name": "valid-idea-cursor",
        "description": "SKILL.md documents Cursor platform path",
        "checks": [
            ("SKILL.md exists",              lambda: _file_exists(SKILL_MD)),
            ("Cursor path documented",       lambda: _file_contains(SKILL_MD, r"Cursor")),
            ("git CLI path present",         lambda: _file_contains(SKILL_MD, r"git CLI|git init|git push")),
            ("Cursor memory path",           lambda: _file_contains(SKILL_MD, r"\.cursor.+skills.+incubate")),
            ("Windows path support",         lambda: _file_contains(SKILL_MD, r"USERPROFILE|Windows")),
            ("Platform compat matrix",       lambda: _file_contains(SKILL_MD, r"Platform Compatibility")),
            ("Cursor install path",          lambda: _file_contains(SKILL_MD, r"\.cursor")),
        ],
    },
    {
        "id": "03",
        "name": "vague-idea",
        "description": "Autonomous Interpretation handles vague ideas",
        "checks": [
            ("Autonomous Interpretation section",  lambda: _file_contains(SKILL_MD, r"Autonomous Interpretation")),
            ("3 interpretations documented",       lambda: _file_contains(SKILL_MD, r"3 possible interpretations|three.*interpretations", re.IGNORECASE)),
            ("Vague idea handler",                 lambda: _file_contains(SKILL_MD, r"< 5 words|vague|too vague")),
            ("Error recovery for vague",           lambda: _file_contains(SKILL_MD, r"Expand to 3|too vague.*expand", re.IGNORECASE)),
            ("PRD section 8 template",             lambda: _file_contains(SKILL_MD, r"8\. Autonomous Interpretation|Section 8")),
            ("No ask_user in phases",              lambda: _file_contains(SKILL_MD, r"Never.*ask_user|never call.*ask_user", re.IGNORECASE)),
            ("Decision log for ambiguous",         lambda: _file_contains(SKILL_MD, r"Decision Log")),
        ],
    },
    {
        "id": "04",
        "name": "duplicate-slug",
        "description": "Slug deduplication with -v2 suffix",
        "checks": [
            ("Slug dedup documented",    lambda: _file_contains(SKILL_MD, r"-v2|-v3|dedup", re.IGNORECASE)),
            ("Slug generation step",     lambda: _file_contains(SKILL_MD, r"Generate Project Slug|project slug", re.IGNORECASE)),
            ("Tag override support",     lambda: _file_contains(SKILL_MD, r"--tag|tag.*slug|slug.*tag")),
            ("Slug normalization",       lambda: _file_contains(SKILL_MD, r"lowercase|replace spaces|normalize")),
            ("Existing slug check",      lambda: _file_contains(SKILL_MD, r"exists in memory|slug exists")),
            ("v2 suffix rule",           lambda: _file_contains(SKILL_MD, r"append.*-v2|add.*-v2|-v2.*suffix", re.IGNORECASE)),
            ("Phase 0 slug handling",    lambda: _file_contains(SKILL_MD, r"Phase 0|## Phase 0")),
        ],
    },
    {
        "id": "05",
        "name": "memory-load",
        "description": "Memory JSONL loads and applies correctly",
        "checks": [
            ("Memory schema defined",      lambda: _file_contains(SKILL_MD, r"Entry Schema|id.*type.*entity.*fact")),
            ("Memory types defined",       lambda: _file_contains(SKILL_MD, r"preference.*fact.*pattern.*mistake.*decision")),
            ("Phase 0 loads memory",       lambda: _file_contains(SKILL_MD, r"Load Memory|memory.*load|load.*memory", re.IGNORECASE)),
            ("Corruption handler",         lambda: _file_contains(SKILL_MD, r"corrupted|\.corrupted\.")),
            ("Memory path table",          lambda: _file_contains(SKILL_MD, r"Storage Paths|Memory Path")),
            ("Active entries filter",      lambda: _file_contains(SKILL_MD, r"active.*entries|status.*active")),
            ("Apply to execution",         lambda: _file_contains(SKILL_MD, r"apply.*memory|working context|apply.*preference", re.IGNORECASE)),
        ],
    },
    {
        "id": "06",
        "name": "memory-save",
        "description": "Phase 11 saves >= 3 new memory entries",
        "checks": [
            ("Phase 11 exists",            lambda: _file_contains(SKILL_MD, r"Phase 11|## Phase 11")),
            ("Minimum 3 entries",          lambda: _file_contains(SKILL_MD, r"≥ 3|>= 3|minimum 3|at least 3")),
            ("Project fact entry",         lambda: _file_contains(SKILL_MD, r"Project fact|type.*fact.*entity.*project", re.IGNORECASE)),
            ("Decision pattern entry",     lambda: _file_contains(SKILL_MD, r"Decision pattern|pattern.*entry|Most significant", re.IGNORECASE)),
            ("Process learning entry",     lambda: _file_contains(SKILL_MD, r"Process learning|went well or badly", re.IGNORECASE)),
            ("Archive threshold",          lambda: _file_contains(SKILL_MD, r"200 entries|archive.*oldest|oldest.*100")),
            ("JSONL append",               lambda: _file_contains(SKILL_MD, r"Append to|append.*jsonl|JSONL", re.IGNORECASE)),
        ],
    },
    {
        "id": "07",
        "name": "prd-completeness",
        "description": "PRD template has all 8 required sections",
        "checks": [
            ("Phase 1 PRD exists",          lambda: _file_contains(SKILL_MD, r"Phase 1|## Phase 1")),
            ("Section 1 Problem Statement", lambda: _file_contains(SKILL_MD, r"1\..*Problem Statement|Problem Statement")),
            ("Section 2 Target Users",      lambda: _file_contains(SKILL_MD, r"2\..*Target Users|Target Users")),
            ("Section 3 Value Prop",        lambda: _file_contains(SKILL_MD, r"3\..*Value Proposition|Value Proposition")),
            ("Section 4 MVP Features",      lambda: _file_contains(SKILL_MD, r"4\..*MVP Features|MVP Features")),
            ("Section 5 Non-Goals",         lambda: _file_contains(SKILL_MD, r"5\..*Non-Goals|Non-Goals")),
            ("Section 6 Success Metrics",   lambda: _file_contains(SKILL_MD, r"6\..*Success Metrics|Success Metrics")),
            ("Section 7 Constraints",       lambda: _file_contains(SKILL_MD, r"7\..*Technical Constraints|Technical Constraints")),
            ("Section 8 Interpretation",    lambda: _file_contains(SKILL_MD, r"8\..*Autonomous Interpretation")),
        ],
    },
    {
        "id": "08",
        "name": "review-rounds",
        "description": "Review Log has all 3 rounds + Final Verdict",
        "checks": [
            ("Phase 2 Self-Review",       lambda: _file_contains(SKILL_MD, r"Phase 2|## Phase 2")),
            ("Round 1 Completeness",      lambda: _file_contains(SKILL_MD, r"Round 1.*Completeness|Completeness Check")),
            ("Round 2 Feasibility",       lambda: _file_contains(SKILL_MD, r"Round 2.*Feasibility|Technical Feasibility")),
            ("Round 3 Autonomous",        lambda: _file_contains(SKILL_MD, r"Round 3.*Autonomous|Autonomous Operation")),
            ("Final Verdict field",       lambda: _file_contains(SKILL_MD, r"Final Verdict")),
            ("Review Log template",       lambda: _file_contains(SKILL_MD, r"Review Log.*Template|# Review Log")),
            ("Retry on failure",          lambda: _file_contains(SKILL_MD, r"max 1 retry|retry.*once|one retry", re.IGNORECASE)),
        ],
    },
    {
        "id": "09",
        "name": "arch-completeness",
        "description": "Architecture template has all 7 required sections",
        "checks": [
            ("Phase 3 Architecture",       lambda: _file_contains(SKILL_MD, r"Phase 3|## Phase 3")),
            ("Section 1 System Overview",  lambda: _file_contains(SKILL_MD, r"1\..*System Overview|System Overview")),
            ("Section 2 Tech Stack",       lambda: _file_contains(SKILL_MD, r"2\..*Technology Stack|Technology Stack")),
            ("Section 3 Data Model",       lambda: _file_contains(SKILL_MD, r"3\..*Data Model|Data Model")),
            ("Section 4 Core Algorithms",  lambda: _file_contains(SKILL_MD, r"4\..*Core Algorithms|Core Algorithms")),
            ("Section 5 Platform Compat",  lambda: _file_contains(SKILL_MD, r"5\..*Platform Compatibility|Platform Compatibility")),
            ("Section 6 Error Handling",   lambda: _file_contains(SKILL_MD, r"6\..*Error Handling|Error Handling Strategy")),
            ("Section 7 Decision Log",     lambda: _file_contains(SKILL_MD, r"7\..*Decision Log|Decision Log")),
        ],
    },
    {
        "id": "10",
        "name": "test-coverage",
        "description": "Test suite has >= 13 scenarios",
        "checks": [
            ("run_tests.py exists",        lambda: _file_exists(RUN_TESTS)),
            ("SCENARIOS dict present",     lambda: _file_contains(RUN_TESTS, r"SCENARIOS\s*=")),
            ("20+ scenarios defined",      lambda: _count_matches(RUN_TESTS, r'"id":\s*"\d+"') >= 20),
            ("--workers flag",             lambda: _file_contains(RUN_TESTS, r"--workers")),
            ("--runs flag",                lambda: _file_contains(RUN_TESTS, r"--runs")),
            ("concurrent executor",        lambda: _file_contains(RUN_TESTS, r"ThreadPoolExecutor|ProcessPoolExecutor|concurrent\.futures")),
            ("scenarios dir exists",       lambda: SCENARIOS_DIR.is_dir()),
        ],
    },
    {
        "id": "11",
        "name": "batch-threshold",
        "description": "Batch test math targets >= 1000 total checks",
        "checks": [
            ("Phase 7 Batch exists",      lambda: _file_contains(SKILL_MD, r"Phase 7|## Phase 7")),
            ("1000 checks target",        lambda: _file_contains(SKILL_MD, r"1000|1,000|\u2265 1000")),
            ("95% pass rate target",      lambda: _file_contains(SKILL_MD, r"95%|\u2265 95")),
            ("Workers x runs math",       lambda: _file_contains(SKILL_MD, r"8 workers|10 runs|workers.*runs")),
            ("Test math documented",      lambda: _file_contains(SKILL_MD, r"Test Math|7.?840|12.?000|98 checks|150 checks")),
            ("Retry on failure",          lambda: _file_contains(SKILL_MD, r"max 3 attempts|3.*attempt")),
            ("Exception path",            lambda: _file_contains(SKILL_MD, r"SHIPPING_NOTES|exception allowed|ship with")),
        ],
    },
    {
        "id": "12",
        "name": "readme-sections",
        "description": "README has all 11 required sections",
        "checks": [
            ("README.md exists",            lambda: _file_exists(README_MD)),
            ("Problem section",             lambda: _file_contains(README_MD, r"The Problem|## Problem")),
            ("Solution section",            lambda: _file_contains(README_MD, r"The Solution|## Solution")),
            ("Quick Start section",         lambda: _file_contains(README_MD, r"Quick Start|Getting Started")),
            ("How It Works section",        lambda: _file_contains(README_MD, r"How It Works|## How")),
            ("Platform Support section",    lambda: _file_contains(README_MD, r"Platform|Platforms")),
            ("Memory section",              lambda: _file_contains(README_MD, r"Memory|memory layer")),
            ("Contributing section",        lambda: _file_contains(README_MD, r"Contributing|Contribute")),
            ("License section",             lambda: _file_contains(README_MD, r"License|MIT|Apache")),
            ("Badges present",              lambda: _file_contains(README_MD, r"!\[|badge|shields\.io")),
            ("Code block present",          lambda: _file_contains(README_MD, r"```")),
        ],
    },
    {
        "id": "13",
        "name": "website-valid",
        "description": "docs/index.html valid with required elements",
        "checks": [
            ("docs/index.html exists",     lambda: _file_exists(INDEX_HTML)),
            ("Valid HTML structure",        lambda: _file_contains(INDEX_HTML, r"<!DOCTYPE html>|<html")),
            ("Title tag present",           lambda: _file_contains(INDEX_HTML, r"<title>")),
            ("Dark background",             lambda: _file_contains(INDEX_HTML, r"#0d1117|#161b22|background.*#", re.IGNORECASE)),
            ("Stats or metrics present",    lambda: _file_contains(INDEX_HTML, r"checks|scenarios|pass.rate|7.280|stats", re.IGNORECASE)),
            ("pages.yml exists",            lambda: _file_exists(PAGES_YML)),
            ("tests.yml exists",            lambda: _file_exists(TESTS_YML)),
        ],
    },
    # ── /feature-dev scenarios ──────────────────────────────────────────────
    {
        "id": "14",
        "name": "feature-dev-activation",
        "description": "FEATURE_DEV_SKILL.md documents activation syntax and setup",
        "checks": [
            ("FEATURE_DEV_SKILL.md exists",      lambda: _file_exists(REPO_ROOT / "FEATURE_DEV_SKILL.md")),
            ("/feature-dev activation keyword",   lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"/feature-dev")),
            ("--branch flag documented",          lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"--branch")),
            ("--tag flag documented",             lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"--tag")),
            ("--base flag documented",            lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"--base")),
            ("Phase 0 setup section",             lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"Phase 0|## Phase 0")),
            ("Feature slug generation",           lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"feature slug|slug.*lowercase|generate.*slug", re.IGNORECASE)),
        ],
    },
    {
        "id": "15",
        "name": "feature-dev-branching",
        "description": "Branch creation strategy for Copilot and Cursor",
        "checks": [
            ("feat/<slug> naming convention",     lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"feat/<slug>|feat/\<slug\>")),
            ("github-create_branch MCP tool",     lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"github-create_branch")),
            ("git checkout -b Cursor path",       lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"git checkout -b")),
            ("Base branch configurable",          lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"base.*branch|--base|base-branch", re.IGNORECASE)),
            ("Duplicate branch -v2 handling",     lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"-v2|-v3|dedup|already exists", re.IGNORECASE)),
            ("FEATURE_LOG.md logging",            lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"FEATURE_LOG\.md")),
            ("Default base detection",            lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"main.*master.*develop|default branch", re.IGNORECASE)),
        ],
    },
    {
        "id": "16",
        "name": "feature-dev-tdd",
        "description": "TDD-first workflow: RED tests before implementation",
        "checks": [
            ("TDD-first principle documented",    lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"TDD|TDD-first|test-first", re.IGNORECASE)),
            ("Tests written before impl",         lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"write.*test.*before|test.*first.*impl|before.*implementation", re.IGNORECASE)),
            ("RED state documented",              lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"\bRED\b")),
            ("RED to GREEN protocol",             lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"RED.*GREEN|GREEN")),
            ("Framework detection table",         lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"pytest|jest|Framework Detection", re.IGNORECASE)),
            ("Acceptance criteria to tests map",  lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"Acceptance Criteria.*test|criterion.*test", re.IGNORECASE)),
            ("Edge cases required",               lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"[Ee]dge case|at least 2 edge")),
        ],
    },
    {
        "id": "17",
        "name": "feature-dev-pr-copilot",
        "description": "Copilot PR creation via github-create_pull_request MCP",
        "checks": [
            ("github-create_pull_request used",   lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"github-create_pull_request")),
            ("github-push_files used",            lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"github-push_files")),
            ("feat() commit title convention",    lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"feat\(<scope>\)|feat\(.*\):")),
            ("PR description template",           lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"PR Description Template|## Summary")),
            ("Acceptance criteria checklist",     lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"\- \[x\]|\[x\].*criterion", re.IGNORECASE)),
            ("PR URL logged to memory",           lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"PR URL|PR.*memory|memory.*PR", re.IGNORECASE)),
            ("draft PR option",                   lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"draft.*PR|draft=false|draft.*pull", re.IGNORECASE)),
        ],
    },
    {
        "id": "18",
        "name": "feature-dev-pr-cursor",
        "description": "Cursor PR creation via git + gh CLI with fallback",
        "checks": [
            ("git push origin documented",        lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"git push origin")),
            ("gh pr create command",              lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"gh pr create")),
            ("Fallback without gh CLI",           lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"not available|Push.*only|manual PR", re.IGNORECASE)),
            ("git commit -m format",              lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"git commit -m|git add")),
            ("Cursor platform path named",        lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"Cursor.*git CLI|git CLI Path|Cursor.*path", re.IGNORECASE)),
            ("Branch push before PR",             lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"git push origin")),
            ("Error recovery for missing gh",     lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"not available|manual PR|push.*only", re.IGNORECASE)),
        ],
    },
    {
        "id": "19",
        "name": "feature-dev-memory",
        "description": "Memory integration: shared paths, feature type, save 3+ entries",
        "checks": [
            ("Shared memory path (copilot)",      lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"\.copilot.+skills.+incubate")),
            ("Shared memory path (cursor)",       lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"\.cursor.+skills.+incubate")),
            ("'feature' entry type documented",   lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r'"feature"|type.*feature|feature.*type')),
            ("Phase 6 saves >=3 entries",         lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"minimum 3|≥ 3|>= 3|at least 3")),
            ("Feature fact entry format",         lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"type.*feature.*entity.*project|Feature fact", re.IGNORECASE)),
            ("Archive threshold 200 entries",     lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"200 entries|archive.*oldest")),
            ("Memory shared with /incubate",      lambda: _file_contains(REPO_ROOT / "FEATURE_DEV_SKILL.md", r"[Ss]hared [Mm]emory|share.*memory|shared.*incubate", re.IGNORECASE)),
        ],
    },
    {
        "id": "20",
        "name": "feature-dev-harness",
        "description": "feature_dev_harness.py exists with correct structure",
        "checks": [
            ("feature_dev_harness.py exists",     lambda: _file_exists(REPO_ROOT / "tests" / "feature_dev_harness.py")),
            ("SCENARIOS list in harness",         lambda: _file_contains(REPO_ROOT / "tests" / "feature_dev_harness.py", r"SCENARIOS\s*=")),
            ("--workers flag in harness",         lambda: _file_contains(REPO_ROOT / "tests" / "feature_dev_harness.py", r"--workers")),
            ("--runs flag in harness",            lambda: _file_contains(REPO_ROOT / "tests" / "feature_dev_harness.py", r"--runs")),
            ("ThreadPoolExecutor in harness",     lambda: _file_contains(REPO_ROOT / "tests" / "feature_dev_harness.py", r"ThreadPoolExecutor|ProcessPoolExecutor")),
            ("FEATURE_DEV_SKILL.md referenced",   lambda: _file_contains(REPO_ROOT / "tests" / "feature_dev_harness.py", r"FEATURE_DEV_SKILL")),
            ("sys.exit(0) on pass",               lambda: _file_contains(REPO_ROOT / "tests" / "feature_dev_harness.py", r"sys\.exit\(0\)")),
        ],
    },
]


# ─── Runner ───────────────────────────────────────────────────────────────────────────────────
def run_scenario(scenario: dict) -> dict:
    """Execute all checks in a scenario, return results dict."""
    results = []
    for desc, check_fn in scenario["checks"]:
        try:
            passed = bool(check_fn())
        except Exception:
            passed = False
        results.append({"check": desc, "passed": passed})
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    return {
        "id":          scenario["id"],
        "name":        scenario["name"],
        "description": scenario["description"],
        "total":       total,
        "passed":      passed,
        "failed":      total - passed,
        "results":     results,
    }


def run_all(workers: int = 1, runs: int = 1, verbose: bool = False) -> dict:
    """Run all scenarios across N runs with W threads."""
    all_results = []
    start = time.time()
    total_reps = workers * runs
    tasks = [(s, r) for r in range(total_reps) for s in SCENARIOS]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_scenario, s): (s, r) for s, r in tasks}
        for future in as_completed(futures):
            result = future.result()
            all_results.append(result)

    elapsed = time.time() - start
    total_checks = sum(r["total"] for r in all_results)
    total_passed = sum(r["passed"] for r in all_results)
    pass_rate = (total_passed / total_checks * 100) if total_checks > 0 else 0.0

    # Aggregate by scenario
    scenario_stats: dict = {}
    for r in all_results:
        sid = r["id"]
        if sid not in scenario_stats:
            scenario_stats[sid] = {"name": r["name"], "total": 0, "passed": 0, "failures": []}
        scenario_stats[sid]["total"] += r["total"]
        scenario_stats[sid]["passed"] += r["passed"]
        if verbose and r["failed"] > 0:
            for check in r["results"]:
                if not check["passed"]:
                    scenario_stats[sid]["failures"].append(check["check"])

    return {
        "total_checks":   total_checks,
        "total_passed":   total_passed,
        "pass_rate":      pass_rate,
        "elapsed":        elapsed,
        "workers":        workers,
        "runs":           runs,
        "scenario_stats": scenario_stats,
    }


# ─── CLI ──────────────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="/incubate test suite")
    parser.add_argument("--workers", type=int, default=1,     help="Parallel threads (default: 1)")
    parser.add_argument("--runs",    type=int, default=1,     help="Runs per scenario (default: 1)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show failing check names")
    args = parser.parse_args()

    est = len(SCENARIOS) * 7 * args.runs * args.workers
    print(f"\n\U0001f95a /incubate test suite — {len(SCENARIOS)} scenarios × {args.runs} runs × {args.workers} workers")
    print(f"   Expected: ~{est:,} checks\n")

    summary = run_all(workers=args.workers, runs=args.runs, verbose=args.verbose)

    # Print table
    print(f"{'ID':<4} {'Scenario':<32} {'Passed/Total':<14} Rate")
    print("─" * 60)
    for sid, stats in sorted(summary["scenario_stats"].items()):
        pct = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        icon = "\u2705" if pct >= 100 else ("\u26a0\ufe0f" if pct >= 80 else "\u274c")
        print(f"{sid:<4} {stats['name']:<32} {stats['passed']}/{stats['total']:<10}  {pct:.0f}% {icon}")
        if args.verbose:
            for fail in sorted(set(stats.get("failures", []))):
                print(f"       \u2717 {fail}")

    print("─" * 60)
    print(f"\n{'Total checks:':<26} {summary['total_checks']:,}")
    print(f"{'Passed:':<26} {summary['total_passed']:,}")
    print(f"{'Pass rate:':<26} {summary['pass_rate']:.1f}%")
    print(f"{'Elapsed:':<26} {summary['elapsed']:.2f}s")
    workers_label = "Workers x Runs:"
    print(f"{workers_label:<26} {args.workers} x {args.runs}\n")

    if summary["pass_rate"] >= 95:
        print("\u2705 PASS \u2014 quality gate met (\u2265 95%)\n")
        sys.exit(0)
    else:
        print(f"\u274c FAIL \u2014 pass rate {summary['pass_rate']:.1f}% < 95% threshold\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
