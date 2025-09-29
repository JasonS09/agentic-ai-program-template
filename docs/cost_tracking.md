# Cost Tracking Guide

## Why Track Cost?
Prevent runaway usage, compare optimization changes, and inform model selection.

## Basic Formula
`total_cost = (prompt_tokens * prompt_rate + completion_tokens * completion_rate) / 1000`

## Suggested Practice
| Stage | Action |
|-------|--------|
| Experiment | Log tokens per run |
| Pre-Demo | Set weekly budget |
| Production Prep | Add alerts on threshold |

## Tooling
Implement helper in `src/llm/costs.py` mapping model → rates.

## Example Log Entry (JSON)
```
{"run_id": "2025-09-29_01", "model": "gpt-4o-mini", "prompt_tokens": 812, "completion_tokens": 204, "est_cost": 0.0023}
```

## Optimization Levers
- Compress system prompt
- Remove redundant few-shot examples
- Use lower-cost model for intermediate critique steps
- Cache embeddings & retrieval chunks

## Dashboard Idea
Aggregate daily total cost, top N expensive runs, cost per metric improvement.

## Pitfalls
- Chasing minimal cost at quality expense
- Ignoring inference latency (time is user cost)

Balance cost with reliability & safety.
