# Architecture: incubate

## 1. System Overview

`incubate` is an **instruction-only agent skill** — its primary artifact is `SKILL.md`, a structured
Markdown file that AI coding agents (GitHub Copilot, Cursor) load as a system-level instruction set.
When an agent invokes the `/incubate` command, it reads and executes the 11-phase pipeline defined
in SKILL.md autonomously, producing a complete, tested, documented GitHub repository from a one-line
project idea.

```
Developer idea
     │
     ▼
Agent reads SKILL.md
     │
     ▼
Phase 0: Memory Load + Platform Detect + Slug Generate
     │
     ├──► Phase 1-3: PRD + Review + Architecture (planning)
     │
     ├──► Phase 4-5: Development + Ship to GitHub (build)
     │
     ├──► Phase 6-7: Test Framework + Batch Tests (quality)
     │
     ├──► Phase 8-9: README + Website + CI (polish)
     │
     └──► Phase 10-11: Verify + Memory Save (close)
                │
                ▼
         Shippable GitHub repo
```

**Runtime:** The agent IS the runtime. SKILL.md is static Markdown; no process or daemon runs.

## 2. Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Skill definition | Markdown (SKILL.md) | Agent-readable; platform-agnostic; version-controlled |
| Memory persistence | JSONL (`user-memory.jsonl`) | Append-only; grep-friendly; no dependencies |
| Test harness | Python stdlib (`re`, `pathlib`, `concurrent.futures`, `argparse`) | No pip installs; runs on embedded Python |
| GitHub integration (Copilot) | GitHub MCP tools (`github-create_repository`, `github-push_files`) | Native to Copilot CLI runtime |
| GitHub integration (Cursor) | `git` CLI + `gh` CLI | Works in any terminal |
| CI/CD | GitHub Actions (YAML) | Zero-cost; integrates with GitHub Pages |
| Website | Vanilla HTML/CSS | Self-contained; no build step; no CDN required |

## 3. Data Model

### Memory Entry Schema (`user-memory.jsonl`)

Each line is a JSON object:

```jsonc
{
  "id": "<uuid-or-timestamp>",
  "type": "preference | fact | pattern | mistake | decision",
  "entity": "<project-slug | 'user' | 'platform'>",
  "fact": "<human-readable statement>",
  "source": "<slug that generated this entry>",
  "created_at": "<ISO-8601>",
  "status": "active | archived"
}
```

**Type definitions:**

| Type | When created | Example |
|------|-------------|---------|
| `preference` | User expresses a persistent preference | `"user prefers MIT license"` |
| `fact` | Objective project fact logged at completion | `"arxiv-cli shipped to codes1gn/arxiv-cli"` |
| `pattern` | Recurring decision or technical approach | `"always use Python stdlib for test harness"` |
| `mistake` | Failure that should not repeat | `"forgot to set SSH remote; used HTTPS, push failed"` |
| `decision` | One-time architectural choice | `"chose Python over Node for arxiv-cli"` |

**Archive rule:** When total entries exceed 200, oldest 100 are renamed `status: archived`.

### Session State Schema (`session.json`)

Ephemeral per-run state (not persisted across sessions):

```jsonc
{
  "slug": "my-tool",
  "idea": "original one-line idea text",
  "platform": "copilot | cursor",
  "phase": 0,
  "ship_complete": false,
  "repo_url": "",
  "test_stats": {
    "total_checks": 0,
    "pass_rate": 0.0,
    "workers": 8,
    "runs": 10,
    "elapsed_seconds": 0.0
  }
}
```

## 4. Core Algorithms

### Phase 0: Slug Generation

```
idea = normalise(input):   lower-case, strip punctuation, replace spaces with "-"
slug = first 32 chars of idea
if slug in existing_memory_slugs:
    slug = slug + "-v2"
    if slug still exists: slug = slug[:-2] + "-v3"   (and so on)
```

### Phase 2: PRD Self-Review Protocol

```
for round in [Completeness, Feasibility, Autonomous-Operation]:
    run_checklist(round)
    if verdict == FAIL:
        attempt_fix()
        rerun_checklist(round)   # max 1 retry
        if still FAIL:
            log mistake to memory
            abort with error message

if all rounds PASS:
    write Final Verdict: PASS
    proceed to Phase 3
```

### Phase 7: Batch Test Quality Gate

```
result = run_tests(workers=8, runs=10)
attempt = 1
while result.pass_rate < 95% and attempt <= 3:
    diagnose failing scenarios
    patch SKILL.md or run_tests.py
    result = run_tests(workers=8, runs=10)
    attempt += 1

if result.pass_rate < 95%:
    write SHIPPING_NOTES.md (documents known failures)
    log mistake to memory
    proceed anyway (quality gate is a check, not a hard blocker)
```

### Phase 8: Autonomous Interpretation (vague input)

```
if len(idea.split()) < 5 or no_clear_noun_verb(idea):
    generate 3 interpretations
    score each on: (market_need × 10) + (inverse_build_complexity × 5)
    select highest score
    document in PRD Section 8
    proceed with selected interpretation
```

## 5. Platform Compatibility

| Platform | Install Path | GitHub Integration | Memory Path | Status |
|----------|-------------|-------------------|-------------|--------|
| GitHub Copilot (macOS/Linux) | `~/.copilot/skills/incubate/SKILL.md` | MCP: `github-*` tools | `~/.copilot/skills/incubate/user-memory.jsonl` | ✅ Supported |
| GitHub Copilot (Windows) | `%USERPROFILE%\.copilot\skills\incubate\SKILL.md` | MCP: `github-*` tools | `%USERPROFILE%\.copilot\skills\incubate\user-memory.jsonl` | ✅ Supported |
| Cursor (macOS/Linux) | `~/.cursor/skills/incubate/SKILL.md` | git CLI + gh CLI | `~/.cursor/skills/incubate/user-memory.jsonl` | ✅ Supported |
| Cursor (Windows) | `%USERPROFILE%\.cursor\skills\incubate\SKILL.md` | git CLI + gh CLI | `%USERPROFILE%\.cursor\skills\incubate\user-memory.jsonl` | ✅ Supported |
| Claude Code | `~/.claude/skills/incubate/SKILL.md` | git CLI + gh CLI | `~/.claude/skills/incubate/user-memory.jsonl` | 🔶 Untested |

## 6. Error Handling Strategy

| Error Scenario | Detection | Recovery |
|---------------|-----------|----------|
| Vague idea (< 5 words) | Word count check in Phase 0 | Expand to 3 interpretations; auto-select highest score |
| Duplicate slug | Memory lookup in Phase 0 | Append `-v2` / `-v3` suffix |
| Corrupted memory JSONL | JSON parse error in Phase 0 | Rename to `.corrupted.YYYYMMDD`; create fresh file |
| PRD self-review FAIL | Round verdict check in Phase 2 | Fix + retry once; if still FAIL, log mistake + abort |
| Test pass rate < 95% | Quality gate in Phase 7 | Fix + retry up to 3 times; ship with SHIPPING_NOTES.md |
| GitHub push fails (HTTPS) | Git push error in Phase 5 | Switch remote to SSH (`git remote set-url origin git@github.com:...`) |
| MCP tool unavailable | Tool call error in Phase 5 | Fall back to Cursor/git-CLI path |
| Memory file missing | File existence check in Phase 0 | Create empty JSONL file and proceed |

## 7. Decision Log

| Date | Decision | Alternatives Considered | Rationale |
|------|---------|------------------------|-----------|
| 2025-05 | SKILL.md as primary artifact | Python CLI, shell script, VS Code extension | Agent-readable Markdown is platform-portable; no install required |
| 2025-05 | JSONL for memory | SQLite, JSON file, plain text | Append-only; no schema migration; grep-friendly; works offline |
| 2025-05 | Python stdlib for tests | pytest, node test, shell assertions | Zero-dependency; works with embedded Python 3.x |
| 2025-05 | 11-phase pipeline | 5-phase, 7-phase, ad-hoc | 11 phases map exactly to the deliverables expected in a quality open-source project |
| 2025-05 | Light-theme website | Dark terminal theme | Better legibility on modern displays; matches product-quality OSS landing pages |
| 2025-05 | GitHub Actions for CI | Jenkins, CircleCI, manual | Zero-cost; native GitHub integration; familiar to target users |
| 2025-05 | No `ask_user` calls | Interactive clarification prompts | Solo developer may not be present; full autonomy is the core value proposition |
