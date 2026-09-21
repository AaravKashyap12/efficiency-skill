---
guidance_version: 2026-09-21
last_verified: 2026-09-21
review_after: 2026-11-21
sources:
  - https://developers.openai.com/codex/models
  - https://developers.openai.com/codex/subagents
  - https://developers.openai.com/codex/pricing
  - https://platform.openai.com/docs/pricing
---

# Codex and OpenAI API

Every row below was read from the official pages listed in the frontmatter on the verification date. Current user or repository instructions override this file.

## Current tiers

API prices are USD per million tokens at the standard service tier. Credits are per million tokens on ChatGPT plans. Messages are the published local-message estimate per five-hour window on ChatGPT Plus.

| Model | API input | API cached | API output | Credits in / cached / out | Plus messages | Official positioning |
| --- | --- | --- | --- | --- | --- | --- |
| `gpt-6-astra` | $10 | $1 | $50 | 250 / 25 / 1,250 | 5 to 45 | Hardest end-to-end work across code, apps, and research with sustained reasoning and judgment |
| `gpt-5.6-sol` | $4 | $0.40 | $20 | 100 / 10 / 500 | 10 to 100 | Complex, open-ended, ambiguous, or high-value work |
| `gpt-5.6-terra` | $2 | $0.20 | $12 | 50 / 5 / 300 | 25 to 200 | Everyday work needing strong reasoning and tool use. Starting point for work previously on GPT-5.5 |
| `gpt-5.6-luna` | $0.20 | $0.02 | $1.20 | 5 / 0.5 / 30 | 250 to 2,000 | Clear, repeatable, high-volume tasks: extraction, classification, transformation, structured summaries, focused coding |

Sol's API pricing is promotional through at least 2026-11-21. GPT-5.5 retires from ChatGPT and Codex on 2026-10-14 and is not a routing target.

Reasoning effort ladder in the CLI: `low`, `medium`, `high`, `xhigh`, `max`, and `ultra` where the model supports it. Official guidance: use the lowest reasoning effort that produces the result you need. GPT-5.5 efforts do not map exactly onto GPT-5.6, so re-check a familiar task at a lower setting after a model change.

## Relative tiers by session model

| Session model | mid | cheap |
| --- | --- | --- |
| Astra | sol | terra for judgment, luna for mechanical and breadth |
| Sol | terra | luna |
| Terra | none | luna |
| Luna | none | none, orchestrate inline |

## Official guidance to apply

- Subagents doc: start with `gpt-5.6` for demanding agents that need planning, tool use, validation, and follow-through. Use `gpt-5.6-terra` for agents that favor speed over depth, such as exploration, read-heavy scans, large-file review, and parallel workers that return distilled results. Use `gpt-5.6-luna` for fast, narrowly scoped agents handling clear, repeatable, or high-volume work.
- Subagents doc: subagent workflows consume more tokens than comparable single-agent runs, because each subagent does its own model and tool work. Use them to keep noisy intermediate output off the main thread and to parallelize read-heavy work. Be careful with parallel write-heavy work.
- Subagents doc effort guide: `high` for agents that trace complex logic or check edge cases such as reviewers. `medium` as the balanced default. `low` when the task is straightforward and speed matters most.
- Models doc: Astra for the hardest end-to-end work. Sol for complex open-ended work. Terra as the pragmatic all-rounder. Luna for clear repeatable tasks. Most tasks do not need Max or Ultra.
- Pricing doc: switching to Terra or Luna for routine tasks extends usage limits.

## Class matrix

| Class | Dispatch | Effort |
| --- | --- | --- |
| mechanical | luna | low |
| breadth-recon | luna | medium |
| judgment-recon | terra | medium |
| implementation, clear shape | terra | medium |
| implementation, multi-file or subtle | sol, or the session model when the session is Sol | medium |
| hard-reasoning | session model, inline | high |
| consequential | session model, inline, final review at high | high |

## Dispatch mechanics

- Codex delegates on a direct request or when applicable `AGENTS.md` or skill instructions request it. This skill counts as such an instruction.
- Built-in agents: `default`, `worker` for implementation, `explorer` for read-heavy exploration.
- Custom agents are TOML files under `~/.codex/agents/` or `.codex/agents/` with required `name`, `description`, and `developer_instructions`, plus optional `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config`.
- Model and effort resolve from an explicit spawn value, then the `[agents]` defaults `default_subagent_model` and `default_subagent_reasoning_effort` in `config.toml`, then the parent's values. A custom agent file's own `model` or `model_reasoning_effort` takes precedence when set. If a model is selected without an effort, the model's default effort applies.
- `agents.max_concurrent_threads_per_session` caps open subagent threads.
- Subagents inherit the parent's sandbox policy and permission mode. A custom agent file can override `sandbox_mode`, for example `read-only`.

## How to see what ran

- Each subagent thread is visible in the app, CLI, and IDE extension and can be opened to inspect its work and returned summary.
- `/status` in the CLI shows remaining plan limits. The usage dashboard at chatgpt.com/codex/settings/usage shows pace and reset times.
