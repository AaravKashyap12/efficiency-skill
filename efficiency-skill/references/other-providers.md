---
guidance_version: 2026-09-21
last_verified: 2026-09-21
review_after: 2026-11-21
sources:
  - https://docs.x.ai/docs/models
---

# Other providers and harnesses

Use this file when the session runs on a provider not covered by the Claude Code or Codex reference, or when the harness mixes providers. Never route to a model from memory. Build a dated row from official pages first.

## Verified rows

| Provider | Model | Input | Output | Context | Reasoning control | Official positioning | Page date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| xAI | `grok-4.6` | $2 per M | $6 per M | 500k | configurable `reasoning_effort` | Flagship for code and everything else. xAI's own answer to which model to choose is Grok 4.6 for all text and code work | 2026-08-21 |

xAI publishes one general model tier as of the page date. In a Grok-only session there is no cheaper model to route down to, so the only routing knob is `reasoning_effort`. Apply the class table from SKILL.md to effort alone: low for mechanical and breadth work, higher for judgment and hard reasoning.

## Procedure for adding a provider

1. Read the provider's official models page and record model IDs, context limits, and any reasoning or effort parameter.
2. Read the provider's official pricing page and record input, cached input, and output prices with the page date.
3. Read the harness documentation for how a subagent's model and effort are set and how they resolve against the parent's settings. If the harness has no subagent model control, routing is effort-only.
4. Record the verification date and a review date no more than two months out.
5. Run the evals before trusting a new row for judgment-recon or implementation classes. A cheaper model earns those classes by passing, not by price.

## Unverified

Mixed-provider harnesses such as Cursor and OpenCode were not verified for this file. Run the procedure above before routing in them. Do not infer one harness's dispatch behavior from another's.
