# Scenario 20: Feature-Dev Harness Tool

## Purpose
Validates that the feature_dev_harness.py test runner exists and implements the same quality standards as the main run_tests.py (parallel workers, scenario-based structure, exit codes, FEATURE_DEV_SKILL.md validation).

## What It Tests
- `tests/feature_dev_harness.py` file exists
- Harness has SCENARIOS list
- `--workers` flag supported
- `--runs` flag supported
- `ThreadPoolExecutor` or equivalent for parallelism
- References FEATURE_DEV_SKILL.md (not SKILL.md)
- Exit code 0 on pass, 1 on fail

## Expected File Patterns
- `feature_dev_harness.py` file exists at `tests/`
- `SCENARIOS` dict/list in harness
- `--workers` argument
- `--runs` argument
- `ThreadPoolExecutor` or `ProcessPoolExecutor`
- `FEATURE_DEV_SKILL_MD` or `FEATURE_DEV_SKILL.md` reference
- `sys.exit(0)` on PASS

## Pass Criteria
All 7 pattern checks match tests/feature_dev_harness.py.
