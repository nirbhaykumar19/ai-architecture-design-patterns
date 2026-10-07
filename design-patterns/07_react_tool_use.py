"""10 - ReAct (Reason + Act + Observe)

Grok reasons, calls a tool (Act), observes the result, and repeats until it can
answer. Uses OpenAI-compatible function calling.  Run:  python 10_react_tool_use.py
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import chat
from tools import TOOLS_IMPL, TOOLS_SCHEMA


def react(goal: str, max_steps: int = 5) -> str:
    messages = [
        {"role": "system", "content":
            "You are an incident investigator. Use tools to gather facts, then explain "
            "the root cause and propose a fix. Think step by step."},
        {"role": "user", "content": goal},
    ]
    for _ in range(max_steps):
        msg = chat(messages, tools=TOOLS_SCHEMA).choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        if not msg.tool_calls:
            return msg.content
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = TOOLS_IMPL[call.function.name](**args)
            print(f"   [act] {call.function.name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(result)})
    return "Reached step limit."


if __name__ == "__main__":
    print(react("Order 12345 failed. Investigate why and recommend a fix."))
