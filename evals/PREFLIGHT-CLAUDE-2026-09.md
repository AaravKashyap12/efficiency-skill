# Evaluation status — 25 September 2026

## Recorded evidence

Claude Code 2.1.114 was available, but no behavioral case completed:

1. An isolated E01 preflight returned `Not logged in · Please run /login`, `is_error: true`, and no inference tokens. Its reported cost was $0; this is an authentication failure, not a successful cheap answer.
2. With the user's configured provider environment applied only to the child process, the `opus` alias initialized as `claude-opus-4-7`, then repeatedly returned `server_error`. The process was terminated after 120.05 seconds without a behavioral response or cost result.
3. Retrying the configured session model `claude-opus-4.6` produced the same server-error retry pattern and was terminated after 120.06 seconds. No behavioral response or cost result was returned.

Selected raw event fields and transcript hashes are in [evidence/preflight-2026-09.json](evidence/preflight-2026-09.json). Personal paths and session IDs are omitted; credentials were never copied into evidence. Full original transcripts remain in the local handoff scratch workspace.

The configured Haiku alias points to an Opus model. A routed call labeled `haiku` would not establish a cheap-tier comparison. Settings and dated provider reference files were left unchanged, as requested. The CLI and actual model aliases also differ from examples in the preserved provider reference.

## Interpretation

- Completed behavioral runs: **0**. Behavioral pass rates: **not available**, not 0% or 100%.
- Requested cases are enumerated in [results-2026-09.csv](results-2026-09.csv) as NOT_RUN. NOT_RUN rows are plans blocked by the recorded preflight, not fabricated executions.
- The authentication preflight's $0 is not a baseline cost. Model costs and savings are unmeasured; absent figures remain blank.
- No E05 retry-trap answer was returned, so neither a silent miss nor a correct response was observed. The trap remains unresolved. Future results must publish either outcome without softening a miss.
- No E12 baseline/skill website pair ran; there is no headline cost comparison.

## Resume after the connection works

Use the same model/effort and clean fixture per condition, explicitly load candidates without reinstalling them, retain transcripts, and independently assess acceptance. Record the actual model behind each dispatch. Do not count aliased Opus calls as Haiku or estimate a provider's billed costs from an unrelated price table. Run the requested repetitions before making efficacy claims or publishing.
