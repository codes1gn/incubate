# Scenario 19: Feature-Dev Memory Integration

## Purpose
Validates that FEATURE_DEV_SKILL.md correctly integrates with the shared memory layer from /incubate, reading preferences and writing feature facts.

## What It Tests
- Memory shared with /incubate (same user-memory.jsonl path)
- Preferences loaded at Phase 0 and applied during execution
- `feature` entry type documented (new type for feature-dev)
- Minimum 3 entries saved at Phase 6
- Feature fact entry saved (type=feature, entity=project)
- Decision pattern entry saved
- Archive threshold (200 entries) respected

## Expected SKILL.md Patterns
- Shared memory path (same as /incubate paths)
- `feature` entry type in schema
- Phase 0 loads preferences from memory
- Phase 6 saves minimum 3 entries
- `type: feature` entry format
- Archive threshold (200 entries)
- `user-memory.jsonl` shared with incubate

## Pass Criteria
All 7 pattern checks match FEATURE_DEV_SKILL.md.
