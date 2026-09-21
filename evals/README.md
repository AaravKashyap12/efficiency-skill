# Efficiency Skill Evals

Real measurements, not vibes. Every case below is run twice per harness: once in a fresh session without the skill (baseline) and once with it. A route is approved for a task class only when the with-skill runs match the baseline pass rate and cost less. Nothing in `efficiency-skill/` should change without a result row that justifies it.

## Setup

1. Install the skill for the harness under test.
   - Claude Code: copy `efficiency-skill/` to `~/.claude/skills/efficiency-skill/`.
   - Codex: copy `efficiency-skill/` to `~/.codex/skills/efficiency-skill/`.
2. Copy `fixture/` to a scratch directory before each run. Cases E03, E07, E08, and E12 modify files. Start every case from a clean copy.
3. Confirm the harness can actually route. In Claude Code, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` must be unset. In Codex, `agents.enabled` must not be `false`.
4. Optional, Claude Code only: install `tools/dispatch-ledger.sh` as a `PreToolUse` hook so every dispatch is logged with its model. See the header of that file.

## Protocol

- Fresh session per run. Clear context between cases.
- Same session model and effort for baseline and skill runs. Record both.
- Three runs per case per condition. Two is the minimum for a provisional verdict.
- For baseline runs, do not mention efficiency, tokens, or subagents in the prompt. Paste the case prompt verbatim.
- For skill runs, paste the same prompt. Do not tell the model which tier to use. The skill has to decide on its own. On Codex, prefix the prompt with one line that names the skill, since Codex loads skills reliably only when asked. See `codex-runbook.md`.
- Capture measurements immediately after the turn ends, before any follow-up.

## What to record

Fill one row per run in `results-template.csv`.

| Column | Where it comes from |
| --- | --- |
| dispatched, dispatch_models, dispatch_efforts | Claude Code: `/tasks` while running, or the ledger file. Codex: open each subagent thread in the app or CLI. |
| main_in_tokens, main_out_tokens, main_cached_tokens, est_cost_usd | Claude Code: `/usage` session block. Codex: `/status` before and after, plus the usage dashboard at chatgpt.com/codex/settings/usage. Subagent tokens are not in the main transcript on either harness. Record what the harness shows and note the gap. |
| wall_seconds | A stopwatch from submit to final message. |
| passed_acceptance | The acceptance check in `cases.md`, run by you, not by the agent. |
| followups_needed | Number of extra prompts you needed before the acceptance check passed. Zero is the target. |

## Reading the results

For each case, compare the three skill rows against the three baseline rows.

- Same pass rate, lower cost: the route is approved. Keep it.
- Same pass rate, higher cost: the delegation gate is too loose for this shape of task. Tighten Step 1 in SKILL.md and re-run.
- Lower pass rate at any cost: the class floor is too low. Raise the floor one tier in the provider reference and re-run.
- Cheap-tier answer looks right but fails the acceptance check: this is the silent-miss failure. Record it in notes verbatim. It is the most important signal in the whole suite.

The trivial case E01 must never dispatch. Cases E09 and E10 must never leave the session model. A skill run that violates either is a failed run regardless of cost.
