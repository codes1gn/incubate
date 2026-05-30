# Scenario 15: Feature-Dev Branching

## Purpose
Validates that FEATURE_DEV_SKILL.md correctly documents the feature branch creation strategy for both Copilot (MCP tools) and Cursor (git CLI).

## What It Tests
- `feat/<slug>` branch naming convention is documented
- Copilot path uses `github-create_branch` MCP tool
- Cursor path uses `git checkout -b` CLI command
- Branch creation from a configurable base branch
- Duplicate branch handling (append `-v2`)
- Branch name logged to FEATURE_LOG.md
- Default base branch detection (`main`, `master`, `develop`)

## Expected SKILL.md Patterns
- `feat/<slug>` naming
- `github-create_branch` in Copilot path
- `git checkout -b` in Cursor path
- Base branch detection/config
- `-v2` dedup on existing branch
- `FEATURE_LOG.md` branch logging

## Pass Criteria
All 7 pattern checks match FEATURE_DEV_SKILL.md.
