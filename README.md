<p align="center">
  <h1 align="center">🥚 incubate</h1>
  <p align="center"><strong>Fully autonomous project incubation — from idea to shipped GitHub repo while you sleep.</strong></p>
</p>

<p align="center">
  <a href="https://github.com/codes1gn/incubate/actions/workflows/tests.yml">
    <img alt="Tests" src="https://github.com/codes1gn/incubate/actions/workflows/tests.yml/badge.svg" />
  </a>
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg" />
  <img alt="Platforms" src="https://img.shields.io/badge/platforms-Copilot%20%7C%20Cursor%20%7C%20Claude-brightgreen" />
  <a href="https://github.com/codes1gn/incubate">
    <img alt="Stars" src="https://img.shields.io/github/stars/codes1gn/incubate?style=social" />
  </a>
</p>

<p align="center">
  <a href="https://codes1gn.github.io/incubate/">Website</a> &bull;
  <a href="#the-problem">Why</a> &bull;
  <a href="#quick-start">Install</a> &bull;
  <a href="#how-it-works">How It Works</a> &bull;
  <a href="#memory-layer">Memory</a> &bull;
  <a href="#platform-support">Platforms</a>
</p>

---

## The Problem

You have a great side project idea on Friday evening. By the time you sit down on Saturday, you've forgotten half the context, spent 2 hours on boilerplate, and shipped nothing. Or you ask an AI to "build it" — and it asks you 20 questions before writing a single line.

```
Without /incubate:                With /incubate:
──────────────────────────────    ──────────────────────────────────────────
You: "build me a CLI tool"        You: /incubate "batch-rename CLI with AI"
Agent: "What language?"           Agent: [Phase 0] Memory loaded. Platform: Copilot.
You: "Python"                     Agent: [Phase 1] PRD complete. 8 sections.
Agent: "What features?"           Agent: [Phase 2] Self-review: 3 rounds. PASS.
You: (explains for 20 min)        Agent: [Phase 3] Architecture: JSONL + CLI.
Agent: "Any auth needed?"         Agent: [Phase 4] Dev complete. Tests passing.
(45 min later, still no code)     Agent: [Phase 5] Shipped → github.com/you/rename-cli
                                  Agent: [Phase 7] 7840 checks. 100% pass.
                                  Agent: [Phase 9] Website live.
                                  You return to a complete project.
```

## The Solution

`/incubate` is a skill for GitHub Copilot, Cursor, and Claude Code that runs a full 11-phase incubation pipeline — PRD, architecture, code, tests, README, and GitHub Pages — without asking you a single question.

```bash
/incubate "personal finance dashboard" --tag finance-dash
# Go make coffee. Come back to a shipped repo.
```

`/feature-dev` is the companion skill for **adding features to existing projects** with a strict TDD-first workflow:

```bash
/feature-dev "add dark mode toggle" --branch feat/dark-mode
# Tests written first. All RED → GREEN. PR opened automatically.
```

## Quick Start

**GitHub Copilot (VS Code)**
```bash
# Copy SKILL.md to your skills folder
cp SKILL.md ~/.github/skills/incubate/SKILL.md
```

**Cursor**
```bash
cp SKILL.md ~/.cursor/rules/incubate.md
```

**Claude Code**
```bash
# Add to global CLAUDE.md or project CLAUDE.md
cat SKILL.md >> ~/CLAUDE.md
```

Then in your IDE:
```
/incubate "your idea here"
```

## How It Works

### `/incubate` — Full Project Pipeline

```
Phase 0  →  Load memory + detect platform (Copilot / Cursor / local)
Phase 1  →  Write PRD (8-section template, no user input needed)
Phase 2  →  Self-review PRD in 3 rounds (Completeness → Feasibility → Autonomy)
Phase 3  →  Design architecture (7 sections + Decision Log)
Phase 4  →  Develop code (self-test checklist: no secrets, all MVP features)
Phase 5  →  Ship to GitHub (MCP tools on Copilot, git CLI on Cursor)
Phase 6  →  Create test framework (20 scenarios, pattern-based checks)
Phase 7  →  Batch test ≥1000 checks at ≥95% pass rate
Phase 8  →  Write README (11-section template)
Phase 9  →  Build GitHub Pages site + CI workflows
Phase 10 →  Generate status report (manual: enable Pages in Settings)
Phase 11 →  Save ≥3 memory entries for future incubations
```

### `/feature-dev` — TDD Feature Pipeline

```
Phase 0  →  Load memory + detect platform + create feat/<slug> branch
Phase 1  →  Write Feature Spec (5 sections: problem, criteria, scope, approach, interpretation)
Phase 2  →  TDD Design: write failing tests (ALL RED before implementation)
Phase 3  →  Implementation: drive tests to GREEN (RED → GREEN protocol)
Phase 4  →  Self-review: 2 rounds (code quality + acceptance criteria coverage)
Phase 5  →  Ship: commit + PR (github-create_pull_request on Copilot / gh pr create on Cursor)
Phase 6  →  Save ≥3 memory entries (feature facts, decision patterns, process learnings)
```

Each phase has hard quality gates. Failures trigger automatic recovery before continuing.

## Platform Support

| Platform | Install Path | Memory Path | Status |
|----------|-------------|-------------|--------|
| GitHub Copilot (VS Code) | `~/.github/skills/incubate/` | `~/.copilot/skills/incubate/data/` | ✅ Tested |
| Cursor | `~/.cursor/rules/incubate.md` | `~/.cursor/skills/incubate/data/` | ✅ Compatible |
| Claude Code | `~/CLAUDE.md` | `~/.claude/skills/incubate/data/` | 🔜 Planned |
| Windows (any) | `%USERPROFILE%\.<platform>\...` | Same with `\` | ✅ Supported |

## Memory Layer

`/incubate` remembers what it learns across incubations:

```json
{"type": "preference", "entity": "user", "fact": "Prefers TypeScript over JavaScript", "confidence": 0.9}
{"type": "pattern",    "entity": "project", "fact": "CLI tools: always add --dry-run flag", "confidence": 0.8}
{"type": "mistake",   "entity": "tool",  "fact": "GitHub Pages needs manual activation", "confidence": 1.0}
```

Each incubation appends ≥3 entries. Future incubations load these and apply them automatically — no configuration required.

**Storage:** `~/.copilot/skills/incubate/data/user-memory.jsonl` (Copilot) or `~/.cursor/skills/incubate/data/user-memory.jsonl` (Cursor)

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `--tag <name>` | auto-slug | Custom slug / resume tag |
| Memory path | `~/.copilot/...` | Platform-specific |
| Workers | 8 | Parallel test workers |
| Runs | 10 | Batch test repetitions |
| Archive threshold | 200 entries | When to compact memory |

Resume an interrupted incubation:
```
/resume finance-dash
```

## Test Results

```
20 scenarios × 7.5 checks × 8 workers × 10 runs = 12,000 checks per validation

Scenario                        Pass Rate
──────────────────────────────────────────
valid-idea-copilot              100% ✅
valid-idea-cursor               100% ✅
vague-idea                      100% ✅
duplicate-slug                  100% ✅
memory-load                     100% ✅
memory-save                     100% ✅
prd-completeness                100% ✅
review-rounds                   100% ✅
arch-completeness               100% ✅
test-coverage                   100% ✅
batch-threshold                 100% ✅
readme-sections                 100% ✅
website-valid                   100% ✅
feature-dev-activation          100% ✅
feature-dev-branching           100% ✅
feature-dev-tdd                 100% ✅
feature-dev-pr-copilot          100% ✅
feature-dev-pr-cursor           100% ✅
feature-dev-memory              100% ✅
feature-dev-harness             100% ✅
──────────────────────────────────────────
Total: 11,760 checks · 100% pass
```

Run: `python tests/run_tests.py --workers 8 --runs 10`
Harness: `python tests/feature_dev_harness.py --workers 8 --runs 10`

## Repository Structure

```
incubate/
├── SKILL.md                    # /incubate — 11-phase project pipeline
├── FEATURE_DEV_SKILL.md        # /feature-dev — 6-phase TDD feature pipeline
├── data/
│   └── user-memory.jsonl       # Session store (gitignored if personal)
├── tests/
│   ├── run_tests.py            # Pattern-based test runner (20 scenarios)
│   ├── feature_dev_harness.py  # /feature-dev harness (8 scenarios)
│   └── scenarios/              # Scenario documentation (01–20)
├── docs/
│   └── index.html              # GitHub Pages landing page
└── .github/workflows/
    ├── tests.yml               # CI: run test suite on push
    └── pages.yml               # CD: deploy GitHub Pages
```

## Contributing

PRs welcome. To add a new scenario: add an entry to `SCENARIOS` in `tests/run_tests.py`, add the corresponding `tests/scenarios/<n>-<name>.md` documentation, then run `python tests/run_tests.py` to verify ≥95% pass rate.

To add `/feature-dev` scenarios: add to `SCENARIOS` in `tests/feature_dev_harness.py` and run `python tests/feature_dev_harness.py`.

For new platform support: update the Memory Protocol and Platform Detection sections in `SKILL.md` and `FEATURE_DEV_SKILL.md`.

## License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).

## Acknowledgements

Inspired by [durable-request](https://github.com/codes1gn/durable-request) (the keep-alive skill), [agent-handoff](https://github.com/codes1gn/agent-handoff) (cross-session memory), and the idea that AI compute can substitute for human weekend hours.

---

<p align="center">
  <sub>11,760 checks · zero runtime dependencies · Copilot + Cursor + Claude · /incubate + /feature-dev · best-of-N compatible</sub>
</p>
