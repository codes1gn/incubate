# Test Scenarios

This directory contains documentation for each of the 13 test scenarios in the `/incubate` test suite.

The actual test logic (pattern checks) is embedded in `../run_tests.py`. These files document the intent and expected behavior for each scenario.

| ID | Scenario | What It Validates |
|----|----------|-------------------|
| 01 | valid-idea-copilot | Copilot platform path in SKILL.md |
| 02 | valid-idea-cursor | Cursor platform path in SKILL.md |
| 03 | vague-idea | Autonomous Interpretation section |
| 04 | duplicate-slug | Slug deduplication with -v2 suffix |
| 05 | memory-load | Memory JSONL load protocol |
| 06 | memory-save | Phase 11 saves ≥ 3 entries |
| 07 | prd-completeness | All 8 PRD sections present |
| 08 | review-rounds | All 3 review rounds + Final Verdict |
| 09 | arch-completeness | All 7 architecture sections |
| 10 | test-coverage | run_tests.py has ≥ 13 scenarios |
| 11 | batch-threshold | ≥ 1000 checks target documented |
| 12 | readme-sections | README has ≥ 11 sections |
| 13 | website-valid | docs/index.html valid + CI present |
