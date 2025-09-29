"""Prompt templating utilities.

Small, dependency-light helpers for variable interpolation and safe block assembly.
"""
from __future__ import annotations
from string import Template
from typing import Dict, Mapping

class PromptTemplate:
    """Lightweight prompt template using Python's Template.

    Example:
        tpl = PromptTemplate("Hello ${name}")
        text = tpl.render({"name": "Alice"})
    """

    def __init__(self, template: str) -> None:
        if not isinstance(template, str):
            raise TypeError("template must be a string")
        self._template = Template(template)
        self.raw = template

    def render(self, variables: Mapping[str, object]) -> str:
        try:
            # Convert values to string lazily
            safe_vars: Dict[str, str] = {k: str(v) for k, v in variables.items()}
            return self._template.substitute(**safe_vars)
        except KeyError as e:
            missing = e.args[0]
            raise KeyError(f"Missing variable: {missing}") from e

    def partial(self, **kwargs: object) -> "PromptTemplate":
        return PromptTemplate(self.render(kwargs))

    def required_variables(self) -> set[str]:
        # Heuristic extraction of $identifiers
        import re
        pattern = re.compile(r"\$(?:{)?([_a-zA-Z][_a-zA-Z0-9]*)")
        return set(pattern.findall(self.raw))


def join_blocks(*blocks: str, separator: str = "\n\n") -> str:
    """Join non-empty trimmed blocks with a separator.

    Empty / whitespace-only blocks are skipped.
    """
    cleaned = [b.strip() for b in blocks if b and b.strip()]
    return separator.join(cleaned)


__all__ = ["PromptTemplate", "join_blocks"]
