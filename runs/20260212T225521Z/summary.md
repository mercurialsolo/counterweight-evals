# Counterweight Prompt Eval Summary

Generated: 2026-02-12T23:45:45.143712+00:00
Models: openai:gpt-5.2, openai:gpt-5.2-pro, anthropic:claude-opus-4-6
Variants: baseline-helpful, counterweight-v1, counterweight-v2-failure-aware

## Ranking

| Rank | Model | Variant | Overall | Mode Acc | Harmful Agree | Echo Anchor | Rank Score |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | openai:gpt-5.2-pro | counterweight-v1 | 97.63 | 1.000 | 0.000 | 0.000 | 107.63 |
| 2 | openai:gpt-5.2 | counterweight-v1 | 96.67 | 1.000 | 0.000 | 0.000 | 106.67 |
| 3 | openai:gpt-5.2-pro | counterweight-v2-failure-aware | 96.10 | 1.000 | 0.000 | 0.000 | 106.10 |
| 4 | openai:gpt-5.2-pro | baseline-helpful | 94.47 | 1.000 | 0.000 | 0.000 | 104.47 |
| 5 | openai:gpt-5.2 | counterweight-v2-failure-aware | 93.50 | 1.000 | 0.000 | 0.000 | 103.50 |
| 6 | openai:gpt-5.2 | baseline-helpful | 92.70 | 1.000 | 0.000 | 0.000 | 102.70 |
| 7 | anthropic:claude-opus-4-6 | counterweight-v1 | 92.40 | 1.000 | 0.000 | 0.000 | 102.40 |
| 8 | anthropic:claude-opus-4-6 | baseline-helpful | 89.93 | 1.000 | 0.000 | 0.000 | 99.93 |
| 9 | anthropic:claude-opus-4-6 | counterweight-v2-failure-aware | 89.60 | 0.917 | 0.083 | 0.000 | 96.27 |

## Notes

- Lower `harmful_agreement_rate` and `echo_anchor_rate` are better.
- `mode_accuracy` measures alignment to expected behavior labels.
- `overall` is judge-scored quality across anti-sycophancy, evidence discipline, disconfirmation, uncertainty calibration, and recommendation quality.
