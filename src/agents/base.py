"""Base agent abstractions.

Intentionally minimal; participants can extend with planning, memory, tooling.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Protocol, Callable
import time


class Tool(Protocol):  # pragma: no cover - interface
    name: str
    description: str
    def __call__(self, **kwargs: Any) -> Any: ...


def timestamp() -> float:
    return time.time()


@dataclass
class AgentEvent:
    at: float
    type: str
    data: Any


@dataclass
class BaseAgent:
    """A very small agent shell.

    Attributes:
        complete_fn: function turning a prompt into a model completion
        events: structured event log for observability
    """
    complete_fn: Callable[[str], str]
    events: List[AgentEvent] = field(default_factory=list)

    def log(self, type_: str, data: Any) -> None:
        self.events.append(AgentEvent(at=timestamp(), type=type_, data=data))

    def run(self, task: str) -> str:
        self.log("task_start", {"task": task})
        prompt = f"You are a helpful agent. Complete the task:\n{task}"
        output = self.complete_fn(prompt)
        self.log("model_output", {"output": output[:500]})
        self.log("task_end", {})
        return output


__all__ = ["BaseAgent", "AgentEvent"]
