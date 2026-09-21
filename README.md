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

Or load `dist/efficiency-skill.skill` in any harness that accepts the packaged format.

## Layout

- `efficiency-skill/SKILL.md` is the portable routing contract.
- `efficiency-skill/references/` holds one dated file per provider with official sources, prices, effort ladders, and dispatch mechanics. Each carries a `review_after` date. Re-verify rows against the cited pages after that date.
- `evals/` holds the test suite: a small Python fixture, twelve cases with acceptance checks, a results template, a Codex runbook, and an optional Claude Code dispatch ledger hook.

## Status

The routing table is sourced but not yet measured. `evals/cases.md` is the proof plan. A route is approved for a task class only when the with-skill runs match the baseline pass rate at lower cost. Results will be published here as they are collected.

## License

MIT
