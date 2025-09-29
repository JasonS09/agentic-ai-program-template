"""Simple tool registry.

Enables controlled exposure of functions callable by agents or LLM outputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Any

@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]

    def __call__(self, **kwargs: Any) -> Any:  # pragma: no cover
        return self.func(**kwargs)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def list(self) -> list[Tool]:
        return list(self._tools.values())

    def as_spec(self) -> list[dict[str, str]]:
        return [
            {"name": t.name, "description": t.description}
            for t in self._tools.values()
        ]


__all__ = ["Tool", "ToolRegistry"]
