"""LLM client abstraction layer.

Provides a single factory to obtain model invocation functions. This remains
minimal to avoid hard provider coupling; participants can extend.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol
import os

# For now avoid importing heavy SDKs if keys not present.

class LLMClient(Protocol):  # pragma: no cover - structural protocol
    def complete(self, prompt: str, **kwargs: Any) -> str: ...


@dataclass
class SimpleEchoClient:
    """Fallback client that echoes prompt (for offline/dev mode)."""
    name: str = "echo"

    def complete(self, prompt: str, **kwargs: Any) -> str:  # pragma: no cover
        return f"[ECHO:{kwargs.get('model','n/a')}] {prompt[:400]}"


def get_openai_client() -> Optional[Any]:  # pragma: no cover - lazy
    if not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        import openai  # type: ignore
        return openai
    except Exception:
        return None


def completion(model: str | None = None):
    """Return a callable performing a basic text completion.

    Usage:
        complete = completion("gpt-4o-mini")
        output = complete("Hello world")
    """
    model_name = model or os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    openai_mod = get_openai_client()

    if openai_mod:
        def _complete(prompt: str, **kwargs: Any) -> str:
            resp = openai_mod.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                **{k: v for k, v in kwargs.items() if v is not None},
            )
            return resp.choices[0].message.content  # type: ignore[attr-defined]
        return _complete

    # Fallback
    echo = SimpleEchoClient(name="echo:" + model_name)
    return echo.complete


__all__ = ["completion", "LLMClient", "SimpleEchoClient"]
