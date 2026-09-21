---
guidance_version: 2026-09-21
last_verified: 2026-09-21
review_after: 2026-11-21
sources:
  - https://platform.claude.com/docs/en/about-claude/models/overview
  - https://platform.claude.com/docs/en/about-claude/pricing
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/model-config
  - https://code.claude.com/docs/en/costs
  - https://code.claude.com/docs/en/skills
  - https://claude.com/blog/claude-model-and-effort-level-in-claude-code
---

# Claude Code and Claude API

Every row below was read from the official pages listed in the frontmatter on the verification date. Prices are USD per million tokens on the Claude API. Current user or repository instructions override this file.

## Current tiers

| Model | Alias | Input | Cache read | Output | Effort levels | Official positioning |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Fable 5.1 | `fable` | $10 | $0.25 | $50 | low, medium, high, xhigh, max | Demanding reasoning and long-horizon agentic work, or when Opus 5 evals at higher effort still fall short |
| Claude Opus 5 | `opus` | $5 | $0.50 | $25 | low, medium, high, xhigh, max | Start here for most workloads. Complex agentic coding |
| Claude Sonnet 5 | `sonnet` | $2 | $0.20 | $10 | low, medium, high, xhigh, max | Best combination of speed and intelligence |
| Claude Haiku 4.5 | `haiku` | $1 | $0.10 | $5 | not supported | Fastest model for simple tasks |

Default effort is `high` on every model that supports it. Fable models, Sonnet 5, and Opus 4.7 and later always use adaptive reasoning. Haiku 4.5 has no effort control.

Cache reads are 0.1x base input on every model except Fable 5.1 and Mythos 5.1, where they are 0.025x. Consequence: from a Fable 5.1 session, a cache-heavy dispatch to Opus pays $0.50 per cached million where the session would have paid $0.25. Opus still halves base input and output. For cache-heavy implementation dispatches from a Fable 5.1 session, measure `model: inherit` against `opus` before assuming Opus is cheaper.

## Relative tiers by session model

| Session model | mid | cheap |
| --- | --- | --- |
| Fable | opus | sonnet for judgment, haiku for mechanical and breadth |
| Opus | sonnet | haiku |
| Sonnet | none | haiku |
| Haiku | none | none, orchestrate inline |

## Official guidance to apply

- Costs doc: Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning. For simple subagent tasks, specify `model: haiku` in the subagent configuration.
- Models overview: start with Opus 5 for most workloads. Use Fable 5.1 for demanding reasoning and long-horizon agentic work.
- Model and effort blog: the model setting is roughly how capable, the effort setting is roughly how thorough. Pick a smaller model for routine work you can describe precisely. Pick a larger model when the smaller one is confidently wrong no matter how much context you give it. Larger models handle ambiguity better; smaller models need specific execution instructions. On hard multi-step work the larger model can cost less per task because it finishes in fewer steps.
- Model config doc: `low` is for short, scoped, latency-sensitive tasks that are not intelligence-sensitive. `medium` trades some intelligence for cost. `max` is prone to overthinking and should be tested before broad use. The effort scale is calibrated per model, so the same name is not the same value across models.

## Class matrix

| Class | Dispatch | Effort |
| --- | --- | --- |
| mechanical | haiku | not applicable |
| breadth-recon | haiku | not applicable |
| judgment-recon | sonnet | low |
| implementation, clear shape | sonnet | medium |
| implementation, multi-file or subtle | opus, or `inherit` from a Fable 5.1 session for cache-heavy work | medium |
| hard-reasoning | session model, inline | high |
| consequential | session model, inline, final review at high | high |

## Dispatch mechanics

- The Agent tool accepts a per-invocation `model` parameter. It has no effort parameter. Effort comes from the subagent definition's `effort` frontmatter or the session level.
- Subagent frontmatter supports `model` (`sonnet`, `opus`, `haiku`, `fable`, a full ID, or `inherit`) and `effort` (`low`, `medium`, `high`, `xhigh`, `max`).
- Model resolution order: per-invocation parameter, then frontmatter `model`, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main conversation's model.
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` with `CLAUDE_CODE_SUBAGENT_MODEL` pins every subagent to one model and makes the Agent tool's model parameter inert. Do not assume routing works while it is set.
- Since v2.1.198 the built-in Explore agent inherits the session model, capped at Opus on the Claude API. A bare Explore dispatch from an Opus or Fable session runs on Opus. To keep exploration cheap, pass `model=haiku` on the dispatch or define a project subagent named `Explore` with `model: haiku`.
- Explore and Plan skip CLAUDE.md and git status. Other subagents load CLAUDE.md unless `omitClaudeMd` is set.
- Subagents inherit the session's extended thinking setting. There is no per-subagent thinking toggle.
- Skills can set `model`, `effort`, and `context: fork` with an `agent` type, which runs the skill in a subagent on that agent's model.
- Changing effort mid-conversation invalidates the cached prompt prefix. Vary effort across dispatches, each with its own context, not inside one conversation.

## How to see what ran

- `/tasks` names the model on each running subagent's row and the effort level when the definition sets one. Requires v2.1.242 or later.
- `/usage` shows the session's token totals, cost estimate at list price, and attribution to skills, subagents, plugins, and MCP servers. The prompt cache line covers the main conversation only.
- Subagent tokens live in their own context and never appear in the main transcript.
