# Scenario 04 — duplicate-slug

**What it validates:** Slug deduplication works correctly when a project with the same slug already exists in memory.

## Behavior
When generating a slug that already exists:
1. Append `-v2` suffix
2. If `-v2` also exists, append `-v3`, etc.
3. Continue without user input

## Checks
- `-v2`/`-v3` suffix strategy is documented
- Slug generation step is in Phase 0
- `--tag` override is documented
- Slug normalization (lowercase, replace spaces) is documented
- Memory check for existing slugs is documented
- v2 suffix rule is explicit
