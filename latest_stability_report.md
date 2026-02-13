# Counterweight Eval Stability Report

Date: 2026-02-13
Source responses: `evals/counterweight/runs/20260212T225521Z/responses.jsonl`
Judge passes:
- `evals/counterweight/runs/20260212T225521Z`
- `evals/counterweight/runs/20260213T003745Z`
- `evals/counterweight/runs/20260213T004226Z`

## Setup
- Cases: 12 (`evals/counterweight/cases.jsonl`)
- Prompt variants:
  - `baseline-helpful`
  - `counterweight-v1`
  - `counterweight-v2-failure-aware`
- Models:
  - `openai:gpt-5.2`
  - `openai:gpt-5.2-pro`
  - `anthropic:claude-opus-4-6`
- Judge: `openai:gpt-5-mini`

## Stable ranking (mean across 3 judge passes)

| Rank | Model | Variant | Mean rank score | Rank SD | Mean overall | Mean harmful agreement |
|---|---|---|---:|---:|---:|---:|
| 1 | openai:gpt-5.2 | counterweight-v1 | 106.41 | 0.98 | 96.41 | 0.000 |
| 2 | openai:gpt-5.2 | counterweight-v2-failure-aware | 105.52 | 1.67 | 95.52 | 0.000 |
| 3 | openai:gpt-5.2-pro | counterweight-v1 | 105.33 | 2.01 | 95.61 | 0.000 |
| 4 | openai:gpt-5.2-pro | counterweight-v2-failure-aware | 105.09 | 0.91 | 95.92 | 0.028 |
| 5 | openai:gpt-5.2-pro | baseline-helpful | 103.18 | 1.06 | 93.18 | 0.000 |
| 6 | anthropic:claude-opus-4-6 | counterweight-v2-failure-aware | 102.60 | 4.49 | 93.71 | 0.028 |
| 7 | openai:gpt-5.2 | baseline-helpful | 101.96 | 1.10 | 91.96 | 0.000 |
| 8 | anthropic:claude-opus-4-6 | counterweight-v1 | 98.55 | 5.57 | 91.04 | 0.056 |
| 9 | anthropic:claude-opus-4-6 | baseline-helpful | 95.88 | 6.28 | 86.99 | 0.028 |

## Variant impact by model (overall mean deltas)
- `openai:gpt-5.2`
  - `counterweight-v1 - baseline`: +4.46
  - `counterweight-v2 - baseline`: +3.57
- `openai:gpt-5.2-pro`
  - `counterweight-v1 - baseline`: +2.43
  - `counterweight-v2 - baseline`: +2.74
- `anthropic:claude-opus-4-6`
  - `counterweight-v1 - baseline`: +4.06
  - `counterweight-v2 - baseline`: +6.72

## Decision
- Default recommendation: `openai:gpt-5.2 + counterweight-v1`
- Alternative: `openai:gpt-5.2 + counterweight-v2-failure-aware` if explicit failure-mode reminders are preferred in prompt text.
- Best Opus pairing in this eval: `claude-opus-4-6 + counterweight-v2-failure-aware`.

## Caveats
- Judge variance is non-trivial; use repeated judge passes and spot human review.
- This suite is synthetic and compact (12 cases); expand with your production cases before broad rollout.
- Harmful agreement stayed low overall, but should remain a release-gating metric.

## Model availability note
- `gpt-5.3` is not present in this account's OpenAI model list as of 2026-02-13.
- Available tested models include `gpt-5.2`, `gpt-5.2-pro`, and `claude-opus-4-6`.
