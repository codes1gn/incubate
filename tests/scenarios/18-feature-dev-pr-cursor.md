# Scenario 18: Feature-Dev PR (Cursor / git CLI Path)

## Purpose
Validates that FEATURE_DEV_SKILL.md documents the Cursor git CLI PR creation path using `git` and `gh` commands.

## What It Tests
- `git push origin feat/<slug>` command is documented
- `gh pr create` command is documented
- Fallback when `gh` is not available (push only + manual PR URL)
- `git commit -m` with structured message
- Cursor platform path clearly separated from Copilot path
- Branch push before PR creation
- Error recovery for missing `gh` CLI

## Expected SKILL.md Patterns
- `git push origin`
- `gh pr create`
- Fallback without `gh` documented
- `git commit` with message format
- Cursor platform mentioned in ship phase
- `git add` before commit

## Pass Criteria
All 7 pattern checks match FEATURE_DEV_SKILL.md.
