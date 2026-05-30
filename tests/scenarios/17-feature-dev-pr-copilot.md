# Scenario 17: Feature-Dev PR (Copilot Path)

## Purpose
Validates that FEATURE_DEV_SKILL.md documents the GitHub Copilot PR creation path using MCP tools (github-create_pull_request).

## What It Tests
- `github-create_pull_request` MCP tool is used for Copilot PR path
- `github-push_files` MCP tool for committing code
- PR title follows `feat(<scope>): <description>` convention
- PR description template is provided
- Base branch is configurable
- PR URL is logged to FEATURE_LOG.md and memory
- Draft PR option is documented

## Expected SKILL.md Patterns
- `github-create_pull_request`
- `github-push_files`
- `feat(<scope>):` commit/PR title pattern
- PR description template with acceptance criteria checklist
- Base branch reference
- PR URL logging

## Pass Criteria
All 7 pattern checks match FEATURE_DEV_SKILL.md.
