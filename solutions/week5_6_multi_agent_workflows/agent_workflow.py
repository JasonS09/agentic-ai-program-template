import operator
import json

from typing import Annotated, List, TypedDict, Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_community.tools import DuckDuckGoSearchRun

# Load environment variables
load_dotenv()

# --- Custom Calculator Tool ---
def basic_calculator(expression: str) -> str:
    """
    Very small calculator that evaluates a simple arithmetic expression.
    Supports +, -, *, /, and parentheses.
    Returns the result as a string.
    """
    try:
        # Only allow safe characters
        allowed = "0123456789+-*/(). "
        if any(ch not in allowed for ch in expression):
            raise ValueError("Unsupported characters in expression.")
        # Evaluate the expression
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


# Instantiate the tool once (so it can be reused)
search_tool = DuckDuckGoSearchRun()

# --- Tool registry ---------------------------------------------------------
# Map tool names to callables and a short description for the LLM
TOOLS: Dict[str, Dict[str, Any]] = {
    "search": {
        "func": search_tool.run,
        "description": "Search the web for a query string. Returns a short summary."
    },
    "calculate": {
        "func": basic_calculator,
        "description": "Evaluate a simple arithmetic expression. Returns the numeric result as a string.",
    },
}

# Define the State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    plan: List[str]
    current_step: int
    results: dict

# Initialize LLM
llm = ChatOllama(model="gpt-oss:20b") #ChatOpenAI(model="gpt-4o-mini")

# --- Planner Node ---
planner_prompt = ChatPromptTemplate.from_template(
    """You are a planner. Given a user request, create a step-by-step plan to answer it.
    Return the plan as a JSON list of strings.
    
    Request: {request}
    
    Plan:"""
)

def planner_node(state: AgentState):
    print("--- Planner Node ---")
    request = state["messages"][-1].content
    chain = planner_prompt | llm
    response = chain.invoke({"request": request})
    
    try:
        # Clean up markdown code blocks if present
        content = response.content.replace("```json", "").replace("```", "").strip()
        plan = json.loads(content)
    except json.JSONDecodeError:
        # Fallback
        plan = [line.strip() for line in response.content.split('\n') if line.strip()]
    
    print(f"Generated Plan: {plan}")
    return {"plan": plan, "current_step": 0, "results": {}}

# --- Updated Executor Prompt -----------------------------------------------
executor_prompt = ChatPromptTemplate.from_template(
    """
You are an executor. For the following step, decide whether to call a tool or to execute the step directly.

Available tools:
{tool_descriptions}

Step: {step}
Previous results: {results}

Respond with a JSON object that contains:
- "action": either "call_tool" or "execute"
- If "call_tool": include "tool" (name) and "params" (dict of arguments)
- If "execute": include "content" (the answer you would give)

Example:
{{
  "action": "call_tool",
  "tool": "search",
  "params": {{"query": "population of Tokyo"}}
}}

or

{{
  "action": "execute",
  "content": "The population of Tokyo is about 14 million."
}}
"""
)

# Helper to format tool descriptions for the prompt
def format_tool_descriptions() -> str:
    lines = []
    for name, info in TOOLS.items():
        lines.append(f"- {name}: {info['description']}")
    return "\n".join(lines)

def executor_node(state: AgentState):
    """
    Executes a single step. The LLM decides whether to call a tool or to
    produce the answer directly. The decision is made by parsing the LLM's
    JSON response.
    """
    print("--- Executor Node ---")
    plan = state["plan"]
    current_step = state["current_step"]
    
    if current_step >= len(plan):
        return {"messages": [AIMessage(content="All steps completed.")]}
        
    step = plan[current_step]
    results = state["results"]
    
    print(f"Executing Step {current_step + 1}: {step}")

    # Ask the LLM to decide what to do
    chain = executor_prompt | llm
    response = chain.invoke(
        {
            "step": step,
            "results": results,
            "tool_descriptions": format_tool_descriptions(),
        }
    )
    
    # Parse the LLM's JSON decision
    try:
        decision = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback: treat as direct execution
        decision = {"action": "execute", "content": response.content}
    
    print(decision)
    action = decision.get("action", "execute")

    if action == "call_tool":
        tool_name = decision.get("tool")
        params = decision.get("params", {})
        tool_info = TOOLS.get(tool_name)

        if not tool_info:
            # Unknown tool – fall back to LLM answer
            result_text = f"Error: unknown tool '{tool_name}'."
        else:
            # Call the tool
            try:
                # The tool function may expect a single positional argument
                # or keyword arguments. We support both.
                if isinstance(params["query"], dict):
                    result_text = tool_info["func"](**params["query"])
                else:
                    result_text = tool_info["func"](params["query"])
            except Exception as e:
                result_text = f"Error calling tool '{tool_name}': {e}"
    else:  # action == "execute"
        result_text = decision.get("content", response.content)

    # Store the result and advance
    results[f"step_{current_step + 1}"] = result_text
    print(result_text)

    return {
        "current_step": current_step + 1,
        "results": results,
        "messages": [AIMessage(content=f"Step {current_step + 1} result: {result_text}")],
    }

# --- Graph Construction ---
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)

workflow.set_entry_point("planner")

workflow.add_edge("planner", "executor")

def should_continue(state: AgentState):
    if state["current_step"] < len(state["plan"]):
        return "executor"
    return END

workflow.add_conditional_edges(
    "executor",
    should_continue,
    {
        "executor": "executor",
        END: END
    }
)

app = workflow.compile()

# --- Main Execution ---
if __name__ == "__main__":
    # Example query
    user_input = "Research the population of Tokyo and New York, then calculate the difference."
    
    inputs = {
        "messages": [HumanMessage(content=user_input)]
    }
    
    print(f"User Request: {user_input}")
    
    for event in app.stream(inputs):
        pass # Output is handled by print statements in nodes