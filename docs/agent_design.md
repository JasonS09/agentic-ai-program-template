# Agent Design Fundamentals

## Core Components
| Component | Responsibility | Example |
|-----------|----------------|---------|
| Perception | Normalize/parse inputs | User text → structured intent |
| Planning | Break goal into steps | High-level plan tree |
| Memory | Persist relevant info | Conversation history store |
| Tooling | Extend capabilities | Web search, DB query |
| Reasoning | Infer intermediate states | Hypothesize missing facts |
| Action Execution | Perform step | Call API, write file |
| Evaluation | Score outputs | JSON validity, factuality |
| Governance | Enforce policies | Output filter, rate limiter |

## Control Loop Pseudocode
```
while not goal_reached and iterations < max_iters:
    observe_state()
    plan = planner.decide(next_goal)
    if plan.requires_tool:
        tool_result = tool_executor.execute(plan.tool, plan.args)
    reasoning = reasoner.reflect(plan, tool_result)
    updated_state = state_updater.apply(tool_result, reasoning)
    if governance.blocked(updated_state):
        escalate_or_abort()
```

## Autonomy Levels
1. Scripted sequence
2. Tool suggestions (human approve)
3. Semi-autonomous loops (bounded iterations)
4. Fully autonomous with guardrails & budget caps

## Memory Strategy
| Type | Lifetime | Storage |
|------|----------|---------|
| Working | Single loop | In-prompt tokens |
| Short-term | Session | Redis / in-memory buffer |
| Long-term | Persistent | Vector store + metadata |

## Safety Considerations
- Explicit tool allowlist
- Hard iteration cap
- Cost/time budget enforcement
- Output classification (toxicity / PII)

## Design Anti-Patterns
| Anti-Pattern | Why Harmful | Alternative |
|--------------|------------|------------|
| Monolithic giant prompt | Unmaintainable, costly | Layered modular prompts |
| No evaluation loop | Stagnant quality | Golden set regression eval |
| Blind tool execution | Security risk | Validate tool schema & intent |
| Infinite loops | Resource drain | Iteration + timeout cap |

## Extensibility Tips
- Use registries for tools & skills
- Keep data schemas explicit (Pydantic or dataclasses)
- Centralize model client selection

## Minimal File Layout Example
```
src/
  agents/base.py
  llm/clients.py
  prompt/templating.py
  tools/registry.py
  eval/metrics.py
```
