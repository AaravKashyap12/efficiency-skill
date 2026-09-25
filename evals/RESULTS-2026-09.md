# Codex behavior results — 25 September 2026

The user authorized evaluation here after Claude Code's provider failed. These are **Codex trials**, not Claude Code results. Claude preflight evidence and the unrun Claude ledger remain in [PREFLIGHT-CLAUDE-2026-09.md](PREFLIGHT-CLAUDE-2026-09.md) and [results-claude-blocked-2026-09.csv](results-claude-blocked-2026-09.csv).

## Method and limits

- One fresh trial agent and clean scratch directory per run; candidates explicitly loaded from copied repository source. No global installation was changed and expected answers were not supplied to the trial agents.
- Owners inherited the same parent model/settings; exact runtime model/effort and usage accounting were not exposed. Baselines omitted candidate instructions. Explicit loading is not an automatic-discovery test.
- Parent assessed returned answers and retained evidence, inspected code/changes, and independently reran changed Python fixtures and HTML parsing. Summaries are labeled as evaluator records; they are not passed off as raw transcript exports.
- The harness allowed four concurrent agents. Trials that could delegate had a worker slot reserved. Root-to-trial dispatch is experimental setup and is not counted as the trial owner's worker use.
- PASS means observed case acceptance; PARTIAL means correct task output but an acceptance dimension remains unverified. Requested worker model/effort is distinct from actual execution metadata. Cost, tokens, and wall-time cells remain blank where not available.
- This small, unblinded sample does not establish general quality or cost superiority. No cost-savings claim is supported. E12 candidate run 1 reports incidental exposure to an unrelated completed math-trial summary from an unfiltered agent listing; its evidence records that limitation. No E12 expected answers were supplied.

## Recorded outcomes

20 trials: 14 PASS, 6 PARTIAL, 0 FAIL. Task-output checks passed in 20/20 runs.

| Case | Condition | Run | Status | Evidence |
| --- | --- | --- | --- | --- |
| E01 | baseline | 1 | PASS | [record](evidence/codex/E01-baseline-1.md) |
| E01 | baseline | 2 | PASS | [record](evidence/codex/E01-baseline-2.md) |
| E01 | skill | 1 | PASS | [record](evidence/codex/E01-skill-1.md) |
| E01 | skill | 2 | PASS | [record](evidence/codex/E01-skill-2.md) |
| E02 | baseline | 1 | PASS | [record](evidence/codex/E02-baseline-1.md) |
| E02 | baseline | 2 | PASS | [record](evidence/codex/E02-baseline-2.md) |
| E02 | skill | 1 | PARTIAL | [record](evidence/codex/E02-skill-1.md) |
| E02 | skill | 2 | PARTIAL | [record](evidence/codex/E02-skill-2.md) |
| E05 | baseline | 1 | PASS | [record](evidence/codex/E05-baseline-1.md) |
| E05 | baseline | 2 | PASS | [record](evidence/codex/E05-baseline-2.md) |
| E05 | skill | 1 | PARTIAL | [record](evidence/codex/E05-skill-1.md) |
| E05 | skill | 2 | PARTIAL | [record](evidence/codex/E05-skill-2.md) |
| E09 | baseline | 1 | PASS | [record](evidence/codex/E09-baseline-1.md) |
| E09 | baseline | 2 | PASS | [record](evidence/codex/E09-baseline-2.md) |
| E09 | skill | 1 | PASS | [record](evidence/codex/E09-skill-1.md) |
| E09 | skill | 2 | PASS | [record](evidence/codex/E09-skill-2.md) |
| E12 | baseline | 1 | PASS | [record](evidence/codex/E12-baseline-1.md) |
| E12 | baseline | 2 | PASS | [record](evidence/codex/E12-baseline-2.md) |
| E12 | skill | 1 | PARTIAL | [record](evidence/codex/E12-skill-1.md) |
| E12 | skill | 2 | PARTIAL | [record](evidence/codex/E12-skill-2.md) |

## Findings that must not be hidden

- E01: the baseline and candidate both answered inline. Candidate loading required extra reads; no cost advantage is established.
- E02: both candidate runs initially encountered zero-test discovery and needed a worker follow-up for the explicit seven-test module. Final counts were correct. Record the extra turn, not just the eventual green result.
- E05: all four runs answered No correctly: 2/2 baseline and 2/2 candidate task-output passes. No silent miss was observed. Candidate runs requested a middle-tier worker and verified source; actual worker identity remains unconfirmed. PaymentError is a sibling of TransientError, which alone is caught.
- E09: all four runs computed A = 1.01 and B = 1.02, explained per-line rounding and binary values above the tie, and proposed aggregate decimal rounding. Both candidate runs kept the reasoning inline; there was no lower-tier reasoning dispatch.
- E12: all four websites passed independent parsing, six-price, and responsive-navigation checks. Each candidate dispatched one implementation worker with exclusive file ownership, then verified/corrected the result after handback. The first candidate added an unnecessary local-font assertion; the second attempted a dependency installation that failed before falling back to the standard library. These overheads remain in the evidence. Requested worker identity cannot prove the backend ran that model.
- No prices or cost percentages were calculated from requested model names. The harness supplied no per-run usage accounting, so the original lower-cost approval criterion remains unestablished.
