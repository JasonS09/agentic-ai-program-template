# Prompt Patterns

| Pattern | When To Use | Skeleton |
|---------|-------------|----------|
| Role Instruction | Steer persona & scope | `You are a concise legal assistant...` |
| Few-Shot Contrast | Disambiguate format or tone | Provide good vs bad examples |
| Chain-of-Thought | Complex reasoning | "Think step by step" (or implicit) |
| Self-Critique | Improve reliability | Ask model to review prior answer |
| JSON Schema Constrained | Structured outputs | Provide explicit JSON with required fields |
| Decomposition | Large problems | Ask model to list sub-tasks first |
| Reflection Loop | Iterative refinement | Feed answer back for critique |
| Guarded Output | Safety / compliance | Include disallowed topics + fallback rule |
| Tool Suggestion | Decide tool vs answer | Ask model to choose from tool list |
| Retrieval Augmented | Ground in facts | Insert context block with delimiter |

## Example: JSON Structured Output
```
SYSTEM: You are a data extraction engine. Respond ONLY with valid JSON.
USER: Extract parties and effective_date from the agreement text.
CONSTRAINTS:
{
  "type": "object",
  "properties": {
    "parties": {"type": "array", "items": {"type": "string"}},
    "effective_date": {"type": ["string", "null"]}
  },
  "required": ["parties", "effective_date"]
}
OUTPUT ONLY JSON.
```

## Example: Reflection Pattern
```
1. Draft answer
2. Critique weaknesses
3. Produce improved final
```

## Prompt Anti-Patterns
| Issue | Symptom | Fix |
|-------|---------|-----|
| Over-specification | Model ignores late instructions | Order by priority, trim noise |
| Hidden constraints | Unstable format | Make schema explicit |
| Unbounded creativity | Hallucinations | Provide context + criteria |
| Excessive few-shot | Token waste | Keep only discriminative examples |

Maintain a personal library in `PROMPT_PLAYBOOK.md` with rationale per iteration.
