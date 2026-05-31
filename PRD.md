# Product Requirements Document: incubate

## 1. Problem Statement

Solo developers carry a graveyard of weekend side-project ideas that never ship. The gap is not
creativity — it is the overhead of spinning up each project from scratch: boilerplate, CI/CD
configuration, README writing, GitHub setup, and test harness creation. A solo developer who
wants to prototype a project on Saturday cannot afford to spend Friday night wiring up structure.
Existing scaffolding tools (cookiecutter, create-react-app, etc.) address one language at a time
and require the developer to be present for every decision. AI coding agents (Copilot, Cursor)
can write code autonomously but lack a repeatable end-to-end project lifecycle protocol that
takes an idea to a shippable, tested, documented GitHub repository without developer intervention.

## 2. Target Users

**Primary:** Solo developer with a backlog of side-project ideas and limited weekend time.

Characteristics:
- Uses GitHub Copilot or Cursor as their primary AI coding assistant
- Has ideas ranging from "CLI tool for X" to "visualizer for Y" — vague to semi-vague
- Values quality output (tested, documented, on GitHub) not just a working prototype
- Does not want to babysit the agent; prefers to come back and review a finished repo

**Secondary:** Small teams incubating internal tools without a dedicated devops/platform engineer.

## 3. Value Proposition

Give the agent a one-line idea. Come back to a fully tested, documented GitHub repo.

- **Zero boilerplate anxiety** — 11-phase pipeline covers PRD → architecture → code → tests → README → website → CI
- **Platform-portable** — works with GitHub Copilot (MCP tools) and Cursor (git CLI)
- **Persistent memory** — learns user preferences (language, license, badge style) across projects
- **Autonomous decision-making** — never calls `ask_user`; resolves ambiguity from context
- **Quality gate** — ≥ 1000 checks at ≥ 95% pass rate before marking a project complete

## 4. MVP Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | 11-phase pipeline | PRD → Self-Review → Architecture → Dev → Ship → Test Framework → Batch Tests → README → Docs Site → Verify → Memory Save |
| 2 | Platform detection | Auto-detects Copilot (MCP) vs Cursor (git CLI) and executes the right path |
| 3 | Memory layer | JSONL-based persistent memory (preferences, facts, decisions, mistakes) per platform |
| 4 | Slug generation | Normalises idea → kebab-case slug; deduplicates with `-v2` suffix |
| 5 | Autonomous interpretation | Expands vague ideas into 3 interpretations; picks most viable without prompting user |
| 6 | Pattern-based test suite | `run_tests.py` with parallel workers, configurable runs, ≥ 95% quality gate |
| 7 | README template | 11-section README covering problem/solution/quick-start/platform/tests/license |
| 8 | GitHub Pages website | Light-theme `docs/index.html` + CI deploy workflow via GitHub Actions |
| 9 | Self-review | 3-round PRD review (completeness, feasibility, autonomous operation) before coding |
| 10 | Memory save | Phase 11 saves ≥ 3 JSONL entries (project fact, decision pattern, process learning) |

## 5. Non-Goals

- **Not a language-specific scaffolder** — no `create-react-app`-style language templates
- **Not a multi-developer workflow tool** — designed for single-agent, single-user sessions
- **Not an interactive interview tool** — the pipeline never pauses to ask the user questions
- **Not a deployment pipeline** — shipping means pushing to GitHub; production infra is out of scope
- **Not a code review tool** — self-review is for PRD quality, not code correctness

## 6. Success Metrics

| Metric | Target |
|--------|--------|
| Time from idea to pushed repo | ≤ 30 minutes per project |
| Test pass rate | ≥ 95% across all scenarios |
| Total checks per run | ≥ 7,840 (13 scenarios × avg 7 checks × 8 workers × 10 runs) |
| Memory persistence | ≥ 3 entries saved per completed project |
| Platform coverage | Copilot (MCP) + Cursor (git CLI) + Windows + macOS/Linux |
| Autonomous completion | 0 `ask_user` calls during pipeline execution |

## 7. Technical Constraints

- **Instruction-only artifact** — the primary deliverable is `SKILL.md`, a Markdown instruction file read by AI agents; no runtime binary or service
- **No external dependencies** — test harness uses Python stdlib only (`re`, `pathlib`, `concurrent.futures`, `argparse`)
- **Platform-agnostic install** — copy skill file to `~/.copilot/skills/incubate/SKILL.md` (Copilot) or `~/.cursor/skills/incubate/SKILL.md` (Cursor)
- **Memory format** — JSONL (one JSON object per line); schema must be stable across versions
- **CI** — GitHub Actions only; no self-hosted runners required

## 8. Autonomous Interpretation

**Vague input expansion:** If the idea is fewer than 5 words or lacks a clear noun + verb, the
pipeline generates 3 possible interpretations ranked by viability score (market need × build
complexity inverse). The highest-scoring interpretation is selected automatically and recorded
in the PRD under this section.

**This project's interpretation:** The idea "autonomous side-project pipeline for AI agents" was
interpreted as: a Markdown skill file that gives AI coding assistants a repeatable 11-phase
project lifecycle, targeting GitHub Copilot and Cursor users on Windows/macOS/Linux, using
git/MCP for GitHub integration and Python stdlib for testing.
