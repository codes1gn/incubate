# Scenario 03 — vague-idea

**What it validates:** The skill handles vague ideas (< 5 words) without asking the user.

## Behavior
When the idea is too short or ambiguous, the skill:
1. Expands it to 3 possible interpretations
2. Chooses the most actionable one
3. Documents the choice in the Decision Log
4. Populates PRD Section 8 (Autonomous Interpretation)

## Checks
- `Autonomous Interpretation` section exists in SKILL.md
- 3-interpretation expansion is documented
- Vague idea handler (`< 5 words`) is in Error Recovery table
- Error recovery for vague idea documents expansion strategy
- PRD Section 8 template includes autonomous interpretation
- `ask_user` is explicitly banned during phases 1-11
- Decision Log is referenced for ambiguous choices
