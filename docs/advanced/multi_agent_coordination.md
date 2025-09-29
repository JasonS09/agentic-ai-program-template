# Multi-Agent Coordination

## Coordination Models
| Model | Description | Use Case |
|-------|-------------|----------|
| Orchestrator | Central planner assigns tasks | Workflow decomposition |
| Blackboard | Shared state, agents post updates | Incremental synthesis |
| Market | Bidding for tasks | Resource optimization |
| Swarm | Local rules, emergent behavior | Creative generation |

## Message Schema
```
{
  "sender": "agent_id",
  "recipient": "agent_id|broadcast",
  "type": "proposal|result|critique|status",
  "content": { ... },
  "trace_id": "uuid"
}
```

## Turn Loop Example
```
for cycle in range(max_cycles):
    for agent in active_agents:
        msg = agent.step(shared_blackboard)
        route(msg)
    if orchestrator.done(shared_blackboard):
        break
```

## Failure Mitigations
| Risk | Strategy |
|------|----------|
| Infinite chatter | Hard cycle cap |
| Role drift | Reassert role in system prompt periodically |
| Conflicting edits | Merge with conflict detection |

## Metrics
- Convergence cycles
- Redundant message ratio
- Contribution diversity (unique agents producing useful updates)

## Optimization
- Prune low-signal agents dynamically
- Summarize long blackboard state periodically

## Safety
Log every inter-agent message for audit & debugging; apply same filtering rules as user-visible outputs.
