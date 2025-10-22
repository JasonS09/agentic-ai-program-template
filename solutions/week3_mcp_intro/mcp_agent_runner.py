"""Agent runner refactored to use optional local LLM (Ollama) and Agnos-style intent parsing.

Enhancements:
1. Attempts structured intent + entity extraction via local Ollama model (e.g., `llama3`).
2. Falls back to regex if local model or parsing fails.
3. Preserves weather tool invocation logic.
4. Returns structured log with which parser was used ("llm" or "regex") and raw LLM parse.

Optional Agnos AI Integration:
If the `agnos` (or `agnos_ai`) library is available, you could adapt the `llm_extract` function
to leverage Agnos task abstractions. Placeholder hook included.

Prerequisites:
`pip install ollama` and ensure the Ollama daemon is running locally.
Pull a model: `ollama pull llama3` (or any supported model)

Environment Overrides:
Set `OLLAMA_MODEL` to change default model.
Set `DISABLE_LLM` to skip LLM parsing even if available.
"""
from __future__ import annotations
import argparse
import json
import re
import os  # Added for environment variable checks
import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, Tuple

# Attempt optional imports (soft-fail)
try:  # Ollama Python client
    from ollama import Client as OllamaClient  # type: ignore
except Exception:  # pragma: no cover
    OllamaClient = None  # type: ignore

try:  # Agnos AI (library name tentative)
    import agnos  # type: ignore
    AGNOS_AVAILABLE = True
except Exception:  # pragma: no cover
    try:
        import agnos_ai as agnos  # type: ignore
        AGNOS_AVAILABLE = True
    except Exception:
        AGNOS_AVAILABLE = False

try:
    from mcp_weather_tool import invoke_get_weather, TOOL_DESCRIPTOR  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("Run from project root so Python can resolve mcp_weather_tool.")

WEATHER_PATTERN = re.compile(r"weather (?:in|at|for) (?P<city>[A-Za-z\-\s]+)\??", re.IGNORECASE)

@dataclass
class InvocationLog:
    query: str
    intent: Optional[str]
    tool_used: bool
    params: Dict[str, Any]
    success: bool
    latency_ms: float
    error: Optional[str]
    answer: str
    parser: str
    llm_raw: Optional[Dict[str, Any]]


def parse_intent_regex(query: str) -> Optional[str]:
    if WEATHER_PATTERN.search(query):
        return "get_weather"
    return None


def extract_city_regex(query: str) -> Optional[str]:
    m = WEATHER_PATTERN.search(query)
    return m.group("city").strip() if m else None


def llm_extract(query: str) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
    """Use local LLM (Ollama) to extract intent + city.

    Returns (intent, city, raw_dict). Falls back to (None, None, {}) on failure.
    """
    if OllamaClient is None:
        return None, None, {}
    if bool(os.getenv("DISABLE_LLM")):
        return None, None, {}
    model = os.getenv("OLLAMA_MODEL", "llama3")
    client = OllamaClient()  # Assumes daemon running
    system_prompt = (
        "You are a parser. Extract weather intent and city. \n"
        "Respond ONLY with JSON: {\n  \"intent\": <string|null>, \n  \"city\": <string|null>\n}.\n"
        "Intent should be 'get_weather' if the user asks for weather for a location."
    )
    user_prompt = f"User Query: {query}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    try:
        resp = client.chat(model=model, messages=messages)
        content = resp.get("message", {}).get("content", "")
        # Attempt to locate JSON substring
        import json, re as _re
        json_match = _re.search(r"\{.*\}", content, flags=_re.DOTALL)
        data: Dict[str, Any] = {}
        if json_match:
            try:
                data = json.loads(json_match.group(0))
            except Exception:
                data = {}
        intent = data.get("intent") if isinstance(data.get("intent"), str) else None
        city = data.get("city") if isinstance(data.get("city"), str) else None
        if intent and not city:
            # LLM marked intent but missed city; attempt regex fallback for city only.
            city = extract_city_regex(query)
        return intent, city, data or {"raw": content}
    except Exception:
        return None, None, {}


def answer_without_tool(query: str) -> str:
    return (
        "I can provide weather if you phrase it like 'weather in <city>'. "
        "Try again specifying a city."
    )


def build_answer_with_tool(query: str, weather: Dict[str, Any]) -> str:
    return (
        f"Weather for {weather['city']}: {weather['temp_c']}°C, {weather['conditions']}. "
        f"(Source: {weather['source']})."
    )


def run_agent(query: str) -> InvocationLog:
    # First attempt LLM-based extraction
    llm_intent: Optional[str]
    llm_city: Optional[str]
    llm_raw: Dict[str, Any]
    intent: Optional[str]
    city: Optional[str]
    parser_used = "regex"

    llm_intent, llm_city, llm_raw = llm_extract(query)
    if llm_intent or llm_city:
        parser_used = "llm"
        intent = llm_intent
        city = llm_city
    else:
        intent = parse_intent_regex(query)
        city = extract_city_regex(query)

    if intent != "get_weather":
        ans = answer_without_tool(query)
        return InvocationLog(query, intent, False, {}, True, 0.0, None, ans, parser_used, llm_raw or None)

    start = time.time()
    params: Dict[str, Any] = {"city": city}
    try:
        if not city:
            raise ValueError("City not detected. Use format 'weather in <city>'.")
        weather = invoke_get_weather(city)
        ans = build_answer_with_tool(query, weather)
        latency = (time.time() - start) * 1000
        return InvocationLog(query, intent, True, params, True, latency, None, ans, parser_used, llm_raw or None)
    except Exception as e:  # pylint: disable=broad-except
        latency = (time.time() - start) * 1000
        return InvocationLog(query, intent, True, params, False, latency, str(e), f"Error: {e}", parser_used, llm_raw or None)


def main():
    parser = argparse.ArgumentParser(description="Minimal MCP-style agent runner")
    parser.add_argument("--query", type=str, required=True, help="User natural language query")
    parser.add_argument("--log-json", type=str, help="Optional path to append JSON log line")
    parser.add_argument("--force-regex", action="store_true", help="Disable LLM parsing even if available")
    args = parser.parse_args()

    if args.force_regex:
        # Temporarily set env to disable LLM usage
        import os
        os.environ["DISABLE_LLM"] = "1"

    log = run_agent(args.query)
    print("Answer:\n" + log.answer)
    print("\nInvocation Log:")
    print(json.dumps(asdict(log), indent=2))

    if args.log_json:
        with open(args.log_json, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(log)) + "\n")
            print(f"Appended log to {args.log_json}")


if __name__ == "__main__":  # pragma: no cover
    main()
