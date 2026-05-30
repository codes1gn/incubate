# Scenario 05 — memory-load

**What it validates:** The memory JSONL file loads correctly at Phase 0 and is applied throughout execution.

## Memory Entry Types
- `preference` — user-level preferences (language, style)
- `fact` — project facts (URLs, names)
- `pattern` — reusable patterns discovered across incubations
- `mistake` — errors logged for future avoidance
- `decision` — significant architectural choices

## Checks
- Entry schema (id, type, entity, fact, confidence, source, created_at, status) is documented
- All 5 entry types are documented
- Phase 0 loads memory from JSONL
- Corruption handler (rename to `.corrupted.`) is documented
- Storage paths table is present
- Active entries filter is documented
- Memory is applied to execution (preferences used)
