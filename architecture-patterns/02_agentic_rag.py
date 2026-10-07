"""02 - Agentic RAG

Retrieval is exposed as a *tool*; OpenAI decides when and what to retrieve,
possibly several times, before composing a cited answer.
Agentic RAG = RAG where the LLM itself decides when, what, and potentially how many times to retrieve information.

User question
     ↓
LLM: "I need EU policy information."
     ↓
Calls TOOL
retrieve("EU refund policy")
     ↓
Gets documents
     ↓
LLM: "I also need UK information."
     ↓
Calls TOOL again
retrieve("UK refund policy")
     ↓
Gets documents
     ↓
LLM: "Now I have enough information."
     ↓
Compares them
     ↓
Final answer


                    AGENT / LLM
                         │
                 "What should I do?"
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Search KB       Database       Send Email
        TOOL             TOOL            TOOL
          │              │              │
          ▼              ▼              ▼
       Python          Python          Python
      function        function        function
      
Run:  python 02_agentic_rag.py
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import chat
from knowledge_base import retrieve

TOOLS = [{
    "type": "function",
    "function": {
        "name": "retrieve",
        "description": "Search the knowledge base for passages relevant to a query.",
        "parameters": {"type": "object",
                       "properties": {"query": {"type": "string"}},
                       "required": ["query"]},
    },
}]


def _retrieve_tool(query: str):
    return [{"id": doc_id, "text": text} for doc_id, text in retrieve(query, k=2)]


def agentic_rag(question: str, max_steps: int = 4) -> str:
    messages = [
        {"role": "system", "content":
            "Answer using the knowledge base. Call `retrieve` as many times as needed "
            "(e.g. once per sub-question), then answer with citations [id]."},
        {"role": "user", "content": question},
    ]
    for _ in range(max_steps):
        msg = chat(messages, tools=TOOLS).choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        if not msg.tool_calls:
            return msg.content
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = _retrieve_tool(**args)
            print(f"   [retrieve] {args['query']} -> {[r['id'] for r in result]}")
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(result)})
    return "Reached step limit."


if __name__ == "__main__":
    print(agentic_rag("Compare our refund policy for EU vs UK customers."))
