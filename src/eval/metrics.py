"""Evaluation metric helpers.

Focused on lightweight, dependency-minimal metrics for early iterations.
"""
from __future__ import annotations
from typing import Any, Mapping
import json
import math


def exact_match(pred: str, gold: str) -> bool:
    return pred.strip() == gold.strip()


def fuzzy_match(pred: str, gold: str) -> bool:
    return pred.strip().lower() == gold.strip().lower()


def json_schema_valid(output: str, schema: Mapping[str, Any]) -> bool:
    try:
        import jsonschema  # type: ignore
    except Exception:  # pragma: no cover
        # Fallback: naive structural check
        try:
            data = json.loads(output)
        except Exception:
            return False
        required = schema.get("required", [])
        return all(k in data for k in required)
    try:
        data = json.loads(output)
        from jsonschema import validate  # type: ignore
        validate(instance=data, schema=schema)  # raises on failure
        return True
    except Exception:
        return False


def token_cost(prompt_tokens: int, completion_tokens: int, model: str, rates: Mapping[str, Any] | None = None) -> float:
    rates = rates or {
        # Example USD per 1K tokens (placeholder - update with real values)
        "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
    }
    model_rates = rates.get(model)
    if not model_rates:
        return math.nan
    return (prompt_tokens * model_rates["prompt"] + completion_tokens * model_rates["completion"]) / 1000.0


__all__ = [
    "exact_match",
    "fuzzy_match",
    "json_schema_valid",
    "token_cost",
]
