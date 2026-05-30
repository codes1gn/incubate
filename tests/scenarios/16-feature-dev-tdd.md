# Scenario 16: Feature-Dev TDD Workflow

## Purpose
Validates that FEATURE_DEV_SKILL.md enforces a strict TDD-first workflow: tests are written before implementation, all tests start RED, and Phase 3 drives them to GREEN.

## What It Tests
- TDD-first principle is documented and mandatory
- Tests written before implementation code
- Tests must be RED at end of Phase 2
- RED → GREEN protocol in Phase 3
- Test framework detection from codebase
- Acceptance criteria map directly to test cases
- Edge cases and error cases covered

## Expected SKILL.md Patterns
- `TDD` or `TDD-first` or `test-first` keyword
- `RED` tests documented as Phase 2 exit state
- `RED.*GREEN` or `GREEN` in Phase 3
- Test framework detection table
- Acceptance Criteria → tests mapping
- Edge case requirement (at least 2)
- Error case requirement

## Pass Criteria
All 7 pattern checks match FEATURE_DEV_SKILL.md.
