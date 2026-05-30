# Scenario 11 — batch-threshold

**What it validates:** The skill documents a batch testing target of ≥ 1000 total checks.

## Test Math
```
13 scenarios × 7 checks = 91 checks/run
91 × 8 workers × 10 runs = 7,280 total checks
```

## Checks
- Phase 7 (Batch Testing) section exists in SKILL.md
- 1000+ checks target is documented
- 95% pass rate threshold is documented
- Workers × runs math is shown
- Test Math section is present
- Retry-on-failure (max 3 attempts) is documented
- Exception path (SHIPPING_NOTES) is documented
