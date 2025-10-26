"""Minimal agent runner that simulates MCP-style tool registration and invocation.

Flow:
1. Load tool descriptor (import from mcp_weather_tool)
2. Parse user natural language query for weather intent (regex/keywords)
3. If intent detected: extract city, invoke tool (function or HTTP)
4. Construct answer citing tool data (avoid hallucination)
5. Log structured record (JSON) for Playbook usage

NOTE: This is an instructional scaffold, not a production MCP client.
"""
from __future__ import annotations
import argparse
import json
import re
import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import requests

from mcp_weather_tool import TOOL_DESCRIPTOR  # type: ignore

OLLAMA_ENDPOINT = "http://localhost:11434/api"
WEATHER_API_ENDPOINT = "http://localhost:8765/weather"
OLLAMA_CONFIG = {"model": "llama3", "stream": False}

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


# def parse_intent(query: str) -> Optional[str]:
#     if WEATHER_PATTERN.search(query):
#         return "get_weather"
#     return None

def get_weather(city: str) -> str:
    """Call the weather API endpoint and return the JSON response as string."""
    try:
        resp = requests.get(f"{WEATHER_API_ENDPOINT}?city={city}")
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[mcp-agent] Error calling weather API: {e}")
        return f"__WEATHER_API_ERROR__ {e}"

def extract_city(query: str) -> Optional[str]:
    m = WEATHER_PATTERN.search(query)
    return m.group("city").strip() if m else None


def answer_without_tool() -> str:
    return (
        "I can provide weather if you phrase it like 'weather in <city>'. "
        "Try again specifying a city."
    )

def call_ollama(prompt: str) -> str:
    """Send a prompt to Ollama generate endpoint and return the model text."""
    try:
        resp = requests.post(f"{OLLAMA_ENDPOINT}/generate", json={"prompt": prompt, **OLLAMA_CONFIG})
        resp.raise_for_status()
        # Ollama payload shape in this repo examples: JSON with "response" field
        data = resp.json() if resp.headers.get("Content-Type", "").startswith("application/json") else json.loads(resp.text)
        return data.get("response", "") if isinstance(data, dict) else str(data)
    except Exception as e:
        return f"__OLLAMA_ERROR__ {e}"


def llm_plan_for_tool(query: str, tool_descriptor: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ask the LLM whether to call the tool. Expect a tiny JSON plan:
      {"action":"get_weather","params":{"city":"Paris"}}
    or:
      {"action":"respond","response":"I cannot help with that."}
    The function tries to parse the model output as JSON and returns a dict fallback on error.
    """
    prompt = (
        "You are an agent with one tool. Tool descriptor:\n"
        f"{json.dumps(tool_descriptor, indent=2)}\n\n"
        f"User query: \"{query}\"\n\n"
        "Decide whether you should call the tool to answer the user. "
        "If you should call the tool, output ONLY valid JSON: "
        '{"action":"get_weather","params":{"city":"<city>"}}. '
        "If you can answer without calling the tool, output ONLY valid JSON: "
        '{"action":"respond","response":"<your answer>"}.\n'
        "Do not output any explanatory text outside the JSON."
    )
    raw = call_ollama(prompt)
    try:
        return json.loads(raw.strip())
    except Exception:
        # fallback: be conservative and ask to call tool if regex matched
        return {"action": "respond", "response": f"Could not parse LLM plan. Raw: {raw}"}


def llm_finalize_answer(query: str, tool_output: Optional[Dict[str, Any]]) -> str:
    """
    Ask the LLM to produce the final answer given the user query and (optional) tool output.
    """
    if tool_output:
        context = json.dumps(tool_output, indent=2)
        prompt = (
            f"User question: \"{query}\"\n\n"
            f"The tool returned:\n{context}\n\n"
            "Using ONLY the tool output and the question, write a concise, non-speculative answer. "
            "Include a short source citation in parentheses, e.g. (Source: mock-weather-service)."
        )
    else:  
        prompt = (
            f"User question: \"{query}\"\n\n"
            "Answer concisely using general knowledge. If unsure, say you are unsure."
        )
    return call_ollama(prompt)


def run_agent(query: str) -> InvocationLog:
    """
    Use the LLM to plan whether to call the weather tool. If the LLM requests a tool call,
    invoke the local tool and then ask the LLM to produce the final answer using the tool output.
    """
    #intent = parse_intent(query)
    plan = llm_plan_for_tool(query, TOOL_DESCRIPTOR)

    start = time.time()
    tool_used = False
    params: Dict[str, Any] = {}
    success = True
    error = None
    answer = ""
    try:
        if plan.get("action") == "get_weather":
            tool_used = True
            params = plan.get("params", {})
            city = params.get("city") or extract_city(query)
            if not city:
                raise ValueError("City not detected (LLM requested tool but did not provide city).")
            params["city"] = city
            weather = get_weather(city)
            # Let LLM craft answer using tool output
            answer = llm_finalize_answer(query, weather)
        elif plan.get("action") == "respond":
            answer = plan.get("response", answer_without_tool())
        else:
            # Unknown plan: fallback
            answer = answer_without_tool()
    except Exception as e:  # pylint: disable=broad-except
        success = False
        error = str(e)
        answer = f"Error: {e}"

    latency = (time.time() - start) * 1000
    return InvocationLog(query, plan.get("action"), tool_used, params, success, latency, error, answer)


def main():
    parser = argparse.ArgumentParser(description="Minimal MCP-style agent runner")
    parser.add_argument("--query", type=str, required=True, help="User natural language query")
    parser.add_argument("--log-json", type=str, help="Optional path to append JSON log line")
    args = parser.parse_args()

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
