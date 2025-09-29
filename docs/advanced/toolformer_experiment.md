# Toolformer-Style Experiment Outline

## Goal
Teach a model to decide when to call tools by labeling training prompts with tool invocation examples.

## Minimal Steps
1. Collect raw text interactions
2. Identify spans where tool use would help
3. Generate synthetic tool call annotations (using a stronger model)
4. Insert annotated examples into few-shot context
5. Evaluate decision precision/recall

## Annotation Format
```
[BEFORE] User: What's the weather in Madrid?
[ANNOTATION] -> TOOL(weather_api, {"location": "Madrid"})
[AFTER] The current temperature is 18°C.
```

## Metrics
| Metric | Description |
|--------|-------------|
| Tool Invocation Rate | % of cases where tool was used |
| Precision | Tool calls that were actually useful |
| Recall | Useful opportunities where tool was used |

## Risks
- Overfitting to synthetic annotation phrasing
- Latency from unnecessary calls

## Extensions
- Add confidence scoring before tool execution
- Penalize redundant tool calls via cost feedback
