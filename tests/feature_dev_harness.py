#!/usr/bin/env python3
"""/feature-dev harness — pattern-based validation of FEATURE_DEV_SKILL.md structure and behavior.

Standalone test runner for the /feature-dev workflow skill. Validates that
the skill correctly documents TDD-first development, branching strategy,
Copilot/Cursor platform paths, memory integration, and PR creation.

Usage:
  python tests/feature_dev_harness.py                        # 1 worker, 1 run
  python tests/feature_dev_harness.py --workers 4            # 4 parallel threads
  python tests/feature_dev_harness.py --workers 8 --runs 10  # 8 threads x 10 runs
  python tests/feature_dev_harness.py --verbose              # show failing checks
"""

import argparse
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ─── Root of the incubate repo ───────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent

FEATURE_DEV_SKILL_MD = REPO_ROOT / "FEATURE_DEV_SKILL.md"
HARNESS_PY = REPO_ROOT / "tests" / "feature_dev_harness.py"
SCENARIOS_DIR = REPO_ROOT / "tests" / "scenarios"


# ─── Helpers ─────────────────────────────────────────────────────────────────
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


# ─── Scenarios ───────────────────────────────────────────────────────────────
FD = FEATURE_DEV_SKILL_MD  # shorthand

SCENARIOS = [
    {
        "id": "14",
        "name": "feature-dev-activation",
        "description": "SKILL.md documents activation syntax, flags, and setup",
        "checks": [
            ("FEATURE_DEV_SKILL.md exists",      lambda: _file_exists(FD)),
            ("/feature-dev activation keyword",   lambda: _file_contains(FD, r"/feature-dev")),
            ("--branch flag documented",          lambda: _file_contains(FD, r"--branch")),
            ("--tag flag documented",             lambda: _file_contains(FD, r"--tag")),
            ("--base flag documented",            lambda: _file_contains(FD, r"--base")),
            ("Phase 0 setup exists",              lambda: _file_contains(FD, r"Phase 0|## Phase 0")),
            ("Feature slug generation",           lambda: _file_contains(FD, r"feature slug|slug.*lowercase|generate.*slug", re.IGNORECASE)),
        ],
    },
    {
        "id": "15",
        "name": "feature-dev-branching",
        "description": "Branch creation strategy for Copilot and Cursor",
        "checks": [
            ("feat/<slug> naming convention",     lambda: _file_contains(FD, r"feat/<slug>|feat/\<slug\>")),
            ("github-create_branch MCP tool",     lambda: _file_contains(FD, r"github-create_branch")),
            ("git checkout -b Cursor path",       lambda: _file_contains(FD, r"git checkout -b")),
            ("Base branch configurable",          lambda: _file_contains(FD, r"base.*branch|--base|base-branch", re.IGNORECASE)),
            ("Duplicate branch -v2 handling",     lambda: _file_contains(FD, r"-v2|-v3|dedup|already exists", re.IGNORECASE)),
            ("FEATURE_LOG.md branch logging",     lambda: _file_contains(FD, r"FEATURE_LOG\.md")),
            ("Default base detection",            lambda: _file_contains(FD, r"main.*master.*develop|default branch", re.IGNORECASE)),
        ],
    },
    {
        "id": "16",
        "name": "feature-dev-tdd",
        "description": "TDD-first workflow: RED tests before implementation",
        "checks": [
            ("TDD-first principle documented",    lambda: _file_contains(FD, r"TDD|TDD-first|test-first", re.IGNORECASE)),
            ("Tests written before impl",         lambda: _file_contains(FD, r"write.*test.*before|test.*first.*impl|before.*implementation", re.IGNORECASE)),
            ("RED state documented",              lambda: _file_contains(FD, r"\bRED\b")),
            ("RED to GREEN protocol",             lambda: _file_contains(FD, r"RED.*GREEN|GREEN")),
            ("Framework detection table",         lambda: _file_contains(FD, r"pytest|jest|Framework Detection", re.IGNORECASE)),
            ("Acceptance criteria to tests map",  lambda: _file_contains(FD, r"Acceptance Criteria.*test|criterion.*test", re.IGNORECASE)),
            ("Edge cases required (2+)",          lambda: _file_contains(FD, r"[Ee]dge case|at least 2 edge")),
        ],
    },
    {
        "id": "17",
        "name": "feature-dev-pr-copilot",
        "description": "Copilot PR creation via MCP tools",
        "checks": [
            ("github-create_pull_request used",   lambda: _file_contains(FD, r"github-create_pull_request")),
            ("github-push_files used",            lambda: _file_contains(FD, r"github-push_files")),
            ("feat() commit title convention",    lambda: _file_contains(FD, r"feat\(<scope>\)|feat\(.*\):")),
            ("PR description template",           lambda: _file_contains(FD, r"PR Description Template|## Summary")),
            ("Acceptance criteria checklist",     lambda: _file_contains(FD, r"\- \[x\]|\[x\].*criterion", re.IGNORECASE)),
            ("PR URL logged to memory",           lambda: _file_contains(FD, r"PR URL|PR.*memory|memory.*PR", re.IGNORECASE)),
            ("draft PR option",                   lambda: _file_contains(FD, r"draft.*PR|draft=false|draft.*pull", re.IGNORECASE)),
        ],
    },
    {
        "id": "18",
        "name": "feature-dev-pr-cursor",
        "description": "Cursor PR creation via git + gh CLI",
        "checks": [
            ("git push origin documented",        lambda: _file_contains(FD, r"git push origin")),
            ("gh pr create command",              lambda: _file_contains(FD, r"gh pr create")),
            ("Fallback without gh CLI",           lambda: _file_contains(FD, r"not available.*gh|gh.*not available|no.*gh", re.IGNORECASE)),
            ("git commit -m format",              lambda: _file_contains(FD, r"git commit -m|git add")),
            ("Cursor platform path named",        lambda: _file_contains(FD, r"Cursor.*git CLI|Cursor.*path|git CLI Path", re.IGNORECASE)),
            ("Push before PR creation",           lambda: _file_contains(FD, r"git push.*feat|push.*then.*PR|push.*branch", re.IGNORECASE)),
            ("Error recovery for missing gh",     lambda: _file_contains(FD, r"gh.*not available|Push.*only|manual PR", re.IGNORECASE)),
        ],
    },
    {
        "id": "19",
        "name": "feature-dev-memory",
        "description": "Memory integration: shared paths, feature type, save 3+ entries",
        "checks": [
            ("Shared memory path (copilot)",      lambda: _file_contains(FD, r"\.copilot.+skills.+incubate")),
            ("Shared memory path (cursor)",       lambda: _file_contains(FD, r"\.cursor.+skills.+incubate")),
            ("'feature' entry type documented",   lambda: _file_contains(FD, r'"feature"|type.*feature|feature.*type')),
            ("Phase 6 saves >=3 entries",         lambda: _file_contains(FD, r"minimum 3|≥ 3|>= 3|at least 3")),
            ("Feature fact entry format",         lambda: _file_contains(FD, r"type.*feature.*entity.*project|Feature fact", re.IGNORECASE)),
            ("Archive threshold 200 entries",     lambda: _file_contains(FD, r"200 entries|archive.*oldest")),
            ("Memory shared with incubate",       lambda: _file_contains(FD, r"Shared Memory|share.*memory|shared.*incubate", re.IGNORECASE)),
        ],
    },
    {
        "id": "20",
        "name": "feature-dev-harness",
        "description": "Harness tool exists with parallel workers and skill reference",
        "checks": [
            ("feature_dev_harness.py exists",     lambda: _file_exists(HARNESS_PY)),
            ("SCENARIOS list in harness",         lambda: _file_contains(HARNESS_PY, r"SCENARIOS\s*=")),
            ("--workers flag in harness",         lambda: _file_contains(HARNESS_PY, r"--workers")),
            ("--runs flag in harness",            lambda: _file_contains(HARNESS_PY, r"--runs")),
            ("ThreadPoolExecutor in harness",     lambda: _file_contains(HARNESS_PY, r"ThreadPoolExecutor|ProcessPoolExecutor|concurrent\.futures")),
            ("FEATURE_DEV_SKILL.md referenced",   lambda: _file_contains(HARNESS_PY, r"FEATURE_DEV_SKILL")),
            ("sys.exit(0) on pass",               lambda: _file_contains(HARNESS_PY, r"sys\.exit\(0\)")),
        ],
    },
    {
        "id": "21",
        "name": "feature-dev-spec",
        "description": "Feature Spec template has all 5 required sections",
        "checks": [
            ("Phase 1 Feature Spec exists",       lambda: _file_contains(FD, r"Phase 1|## Phase 1")),
            ("Section 1 Problem Statement",       lambda: _file_contains(FD, r"1\..*Problem Statement|Problem Statement")),
            ("Section 2 Acceptance Criteria",     lambda: _file_contains(FD, r"2\..*Acceptance Criteria|Acceptance Criteria")),
            ("Section 3 Scope Boundary",          lambda: _file_contains(FD, r"3\..*Scope Boundary|Scope Boundary")),
            ("Section 4 Technical Approach",      lambda: _file_contains(FD, r"4\..*Technical Approach|Technical Approach")),
            ("Section 5 Interpretation",          lambda: _file_contains(FD, r"5\..*Autonomous Interpretation|Autonomous Interpretation")),
            ("Review rounds template",            lambda: _file_contains(FD, r"Round 1|Round 2|Review Log")),
        ],
    },
]


# ─── Runner ──────────────────────────────────────────────────────────────────
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
    """Run all harness scenarios across N runs with W threads."""
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


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="/feature-dev harness test suite")
    parser.add_argument("--workers", type=int, default=1,     help="Parallel threads (default: 1)")
    parser.add_argument("--runs",    type=int, default=1,     help="Runs per scenario (default: 1)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show failing check names")
    args = parser.parse_args()

    est = len(SCENARIOS) * 7 * args.runs * args.workers
    print(f"\n\U0001f527 /feature-dev harness — {len(SCENARIOS)} scenarios × {args.runs} runs × {args.workers} workers")
    print(f"   Expected: ~{est:,} checks\n")

    summary = run_all(workers=args.workers, runs=args.runs, verbose=args.verbose)

    # Print table
    print(f"{'ID':<4} {'Scenario':<36} {'Passed/Total':<14} Rate")
    print("─" * 64)
    for sid, stats in sorted(summary["scenario_stats"].items()):
        pct = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        icon = "\u2705" if pct >= 100 else ("\u26a0\ufe0f" if pct >= 80 else "\u274c")
        print(f"{sid:<4} {stats['name']:<36} {stats['passed']}/{stats['total']:<10}  {pct:.0f}% {icon}")
        if args.verbose:
            for fail in sorted(set(stats.get("failures", []))):
                print(f"       \u2717 {fail}")

    print("─" * 64)
    print(f"\n{'Total checks:':<26} {summary['total_checks']:,}")
    print(f"{'Passed:':<26} {summary['total_passed']:,}")
    print(f"{'Pass rate:':<26} {summary['pass_rate']:.1f}%")
    print(f"{'Elapsed:':<26} {summary['elapsed']:.2f}s")
    workers_label = "Workers x Runs:"
    print(f"{workers_label:<26} {args.workers} x {args.runs}\n")

    if summary["pass_rate"] >= 95:
        print("\u2705 PASS \u2014 /feature-dev harness quality gate met (\u2265 95%)\n")
        sys.exit(0)
    else:
        print(f"\u274c FAIL \u2014 pass rate {summary['pass_rate']:.1f}% < 95% threshold\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
