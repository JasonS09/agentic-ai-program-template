# Evaluation Guide

## Why Evaluate?
Evaluation converts subjective impressions into measurable progress, enabling iterative improvement and preventing regressions.

## Evaluation Layers
| Layer | Goal | Example Metric |
|-------|------|----------------|
| Structural | Valid format | JSON parses |
| Syntactic | Expected fields | Key presence rate |
| Semantic | Factual / correct | Exact match / F1 |
| Reasoning | Quality of steps | Step validity score |
| Safety | Policy adherence | Toxicity flag rate |
| Cost | Efficiency | Tokens / request |

## Dataset Construction
Small but diverse golden sets beat large random collections.
- 5–15 core “anchor” cases
- 5 contrast (edge) cases
- 3 adversarial (stress) cases

## Example Golden Record (JSONL)
```
{"id": "case_01", "input": "User request text", "expected": {"answer": "..."}, "category": "anchor"}
```

## Scoring Functions (`src/eval/metrics.py`)
- `exact_match(pred, gold)`
- `fuzzy_match(pred, gold)` (case/whitespace-insensitive)
- `json_schema_valid(output, schema)`
- `token_cost(prompt_tokens, completion_tokens, model)`

## Process Loop
1. Generate outputs for dataset
2. Compute metrics
3. Inspect failures → categorize root cause
4. Adjust prompt / retrieval / reasoning
5. Re-run evaluation

## Logging Results
Store per run:
```
run_id, timestamp, model, dataset_size, pass_rate, cost_estimate
```
Append JSON lines to `eval/results/<date>-<run>.jsonl`.

## Interpreting Failures
| Failure Type | Cause | Remedy |
|--------------|-------|--------|
| Missing field | Prompt unclear | Add explicit schema & required list |
| Hallucinated fact | No grounding | Inject retrieval context |
| Inconsistent tone | Ambiguous style | Provide tone example |
| Long tail errors | Few edge cases | Add targeted contrast examples |

## Automation
Add a GitHub Action to run a smoke evaluation on a 3–5 case subset to catch gross regressions.

## Caution
Avoid optimizing solely to tests—refresh dataset periodically to prevent overfitting.
