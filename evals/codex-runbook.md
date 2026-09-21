# Codex Runbook

Copy-paste prompts for running the suite on Codex. Baseline and skill runs use the same case prompt. The only difference is the one-line prefix on skill runs.

## One-time setup

Run these in a terminal, not in Codex, so Codex never sees the eval files being staged.

```bash
mkdir -p ~/.codex/skills && cp -r "/c/Users/aarav/Desktop/efficiency skill/efficiency-skill" ~/.codex/skills/
```

```bash
grep -n "enabled" ~/.codex/config.toml
```

If that grep shows `agents.enabled = false`, remove or flip it. If it shows nothing, subagents are on by default.

Check your session model and effort once and write them into every CSV row. Use the picker beneath the composer in the app, or `codex -m <model>` in the CLI. Keep them identical for baseline and skill runs.

## Before every case

Fresh fixture, fresh session.

```bash
rm -rf ~/eval-run && mkdir -p ~/eval-run && cp -r "/c/Users/aarav/Desktop/efficiency skill/evals/fixture/." ~/eval-run/ && cd ~/eval-run && codex
```

Run `/status` first and note the remaining usage figures. That is your before number.

## Baseline run

Paste the case prompt from `cases.md` exactly as written. Nothing else.

## Skill run

Paste this prefix, then the case prompt on the next line:

```
Use the efficiency-skill skill for this task.
```

Do not say which model or tier to use. Do not mention tokens or cost. The skill has to decide.

## After every turn, before any follow-up

1. Run `/status` again. The difference from your before number is the run's usage. Record it in `est_cost_usd` as credits or messages, whichever the plan shows, and say which in notes.
2. Open every subagent thread Codex surfaced in the main thread. Record each thread's model and reasoning effort in `dispatch_models` and `dispatch_efforts`. Zero threads means `dispatched = n`.
3. Run the case's acceptance check yourself from `cases.md`. Do not ask Codex whether it passed.
4. Only then, if the acceptance check failed, send a follow-up and increment `followups_needed`.

Optional after step 2, as a self-report cross-check only:

```
List every subagent you spawned this session with its model and reasoning effort, or say none.
```

Treat that answer as a claim. The thread list is the record.

## Order of cases

Run E01 through E09 as independent sessions. Run E10 in the same session as E07, immediately after E07's acceptance check passes. Run E11 as one session with the four prose turns first. Run E12 last.

Three runs per case per condition. Two is the minimum for a provisional row.

## What decides the result

- E01 dispatches anything: skill run failed.
- E09 or E10 reasoning ran in a subagent thread: skill run failed.
- E05 answered yes: record the thread's model. If it was luna, that is the headline finding.
- E12 with the skill costs more than E12 without and passes the same check: the gate is too loose. Say so in notes.
