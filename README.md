# efficiency-skill

An Agent Skill that routes each task to the cheapest model tier and reasoning effort that holds output quality. The session model you picked stays in charge and delegates bounded work to subagents on smaller models, or answers inline when delegating would cost more. Works in Claude Code, Codex, and any other harness that reads `SKILL.md`.

Every model name, price, and harness rule in the skill comes from the vendor's official documentation, read on a recorded date. Nothing is written from memory.

## What it does

- Classifies each task into one of six classes: mechanical, breadth-recon, judgment-recon, implementation, hard-reasoning, consequential. Each class has a floor tier that work never routes below.
- Applies a delegation gate first. Trivial answers, answers already in context, and tasks that would need the whole conversation to brief stay inline. Delegation has a fixed overhead and the skill refuses to manufacture dispatches.
- Treats model tier and reasoning effort as separate knobs. Effort steps down before tier steps down.
- Keeps hard reasoning, security, money, migrations, and final review on the session model at high effort.
- Requires cheap-tier claims to come back with file and line evidence before the orchestrator builds on them.

## Install

Claude Code:

```bash
cp -r efficiency-skill ~/.claude/skills/
```

Codex:

```bash
cp -r efficiency-skill ~/.codex/skills/
```

`dist/efficiency-skill.skill` packages the 0.2.0 skill source and provider references. Its file set and file bytes were verified against the source folder during release preparation.

## Layout

- `efficiency-skill/SKILL.md` is the portable routing contract.
- `efficiency-skill/references/` holds one dated file per provider with official sources, prices, effort ladders, and dispatch mechanics. Each carries a `review_after` date. Re-verify rows against the cited pages after that date.
- `evals/` holds the test suite: a small Python fixture, twelve cases with acceptance checks, a results template, a Codex runbook, and an optional Claude Code dispatch ledger hook.

## Status

The routing table is sourced but not yet measured. `evals/cases.md` is the proof plan. A route is approved for a task class only when the with-skill runs match the baseline pass rate at lower cost. Only observed results will be published; the pre-launch status is recorded below.

## Results — September 2026 pre-launch

Twenty isolated Codex trials compared baseline and candidate behavior for E01, E02, E05, E09, and E12, twice per condition. Recorded outcomes: 14 PASS, 6 PARTIAL, 0 FAIL. See the [case records and interpretation](evals/RESULTS-2026-09.md) and [CSV](evals/results-2026-09.csv); PARTIAL is not a full acceptance pass.

Both routed E02 runs needed a follow-up after initially discovering zero tests. Worker model/effort overrides are recorded as requested values; actual backend identities and per-run costs were not exposed. No dollar savings, cheaper-tier execution claim, or route approval is established. E05's actual answers and any silent misses remain visible in the records. The website comparisons verify artifacts and requested routing only, not cost superiority.

The originally requested Claude Code measurements remain blocked by authentication/provider failures, recorded separately. Dated provider references are unchanged. These Codex trials do not stand in for Claude Code cost measurements.

## Pairing with engineering workflows

Routing governs dispatch, tier, and effort. An engineering workflow governs code ownership, verification, and completion. Keep one owner per file and consequential decisions with the session owner; bounded workers return evidence without recursive reviewer loops.

## License

MIT
