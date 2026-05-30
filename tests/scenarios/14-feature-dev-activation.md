# Scenario 14: Feature-Dev Activation

## Purpose
Validates that FEATURE_DEV_SKILL.md documents the correct activation syntax, branch/tag flags, platform detection, and memory load at startup.

## What It Tests
- `/feature-dev <description>` activation syntax is documented
- `--branch` override flag is documented
- `--tag` slug override is documented
- `--base` branch override is documented
- Platform detection (Copilot vs Cursor) is documented
- Memory load on Phase 0 activation
- Feature slug generation

## Expected SKILL.md Patterns
- `/feature-dev` activation keyword
- `--branch`, `--tag`, `--base` flags
- `Phase 0` setup section
- Platform detection table
- Memory load step in Phase 0
- Feature slug generation (lowercase, `-`, truncate)
- Branch deduplication (`-v2` suffix)

## Pass Criteria
All 7 pattern checks match FEATURE_DEV_SKILL.md.
