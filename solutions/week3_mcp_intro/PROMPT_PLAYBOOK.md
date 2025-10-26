# Prompt Playbook v1 - Week 3

| Query                                        | Intent Parsed | Tool? | Tool Latency ms | Success | Answer Quality (1–5) | Notes                                                                                                                                           |
| -------------------------------------------- | ------------- | ----- | --------------- | ------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| What is the weather in Madrid?               | get_weather   | Yes | 4652.84         | True  | **5**                | Perfect execution: intent detected, city parsed correctly, tool invoked, JSON parsed, and answer cited the mock-weather-service source clearly. |
| What is the weather in San Jose, Costa Rica? | get_weather   | Yes | 4735.77         | True  | **5**                | Correct multi-word city parsing (“San Jose”), good source attribution, fluent natural language output, accurate tool data.                      |
| What is the weather in Lima?                 | get_weather   | Yes | 4754.13         | True  | **5**                | City extracted correctly, data accurately reflected, explicit citation present, consistent format.                                              |
| What is the weather in this place?           | respond       | No  | 0.0             | True  | **4**                | Correctly avoided calling the tool; graceful fallback message. Minor improvement: could clarify it needs a city name explicitly.                |
| What time is it in New York?                 | respond       | No  | 0.0             | True  | **5**                | Correct refusal; intent properly rejected as non-weather query, preventing false positive tool use. Excellent boundary handling.                |


Success Criteria:
- Tool invoked only when needed
- City parameter extracted correctly (≥3 test cities)
- Error handled (unknown city) without crash
- Answer cites tool data explicitly (e.g., “According to tool…”) 

---
## Failure Modes
| Mode | Description | Mitigation |
|------|-------------|------------|
| False Positive | Tool called when no weather intent | Better intent classifier / threshold |
| False Negative | Missed weather query | Expand pattern list / few-shot examples |
| Hallucinated Data | Answer fabricates temps | Enforce explicit citation from result JSON |
| Stale Response | Cached outdated value | Cache invalidation timeout |
| Tool Error Leak | Raw traceback in answer | Wrap exceptions, return friendly message |

## Reflection Prompts
- When did the tool invocation NOT improve answer quality?
None. Every valid weather query was handled cleanly and enriched by tool data.

- Which failure mode appeared first? Root cause?
None; all queries produced graceful fallbacks.

- Next production hardening step you’d prioritize?
Implement a parameter clarification prompt when location entity extraction fails, e.g.,
“Could you tell me which city you’re asking about?”
This could improve robustness against underspecified user inputs.