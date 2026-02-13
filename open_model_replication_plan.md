# Open-Model Replication Plan

## Why run this

Frontier-model runs are expensive and judge variance exists. Running many repeats on smaller models gives a cheaper estimate of whether the prompt effect is robust.

## Recommended setup

- Keep the same 12-case suite and 3 prompt variants.
- Add 3-5 lower-cost open(-weights) models through an API gateway or local serving.
- Run each model/variant pair with multiple repeats (minimum 5, target 10).
- Aggregate by mean and confidence intervals for:
  - `overall_100`
  - `harmful_agreement_rate`
  - `mode_accuracy`

## Candidate model set

- `meta-llama/llama-3.3-70b-instruct`
- `qwen/qwen2.5-72b-instruct`
- `mistralai/mixtral-8x22b-instruct`
- `deepseek/deepseek-r1-distill-llama-70b`

Use whichever IDs are available in your serving stack.

## Run design

- Phase A (screening): 5 repeats/model/variant on full 12 cases.
- Phase B (confirmatory): top 2 models + top 2 variants, 10 additional repeats.
- Promotion rule:
  - Harmful agreement stays near zero.
  - Variant lift over baseline remains positive across repeats.
  - No severe regressions on safety-health and compliance cases.

## Practical tips

- Keep `temperature=0` for generation unless you explicitly want sampling variance.
- Use repeated independent judge passes even with deterministic generation.
- Track both mean and worst-case run, not mean only.
