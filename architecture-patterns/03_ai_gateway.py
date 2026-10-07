"""03 - AI Gateway

One entry point routes each request to the right model tier (cheap vs frontier)
and keeps a central usage/cost ledger.  Run:  python 03_ai_gateway.py
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import CHEAP_MODEL, DEFAULT_MODEL, chat

# Illustrative prices in USD per 1M tokens: (input, output). Edit to your contract.
PRICES = {
    DEFAULT_MODEL: (3.0, 15.0),
    CHEAP_MODEL: (0.3, 0.5),
}
CHEAP_KINDS = {"classify", "extract", "route", "format"}
_ledger = {"usd": 0.0, "calls": 0}


def choose_tier(task_kind: str) -> str:
    return CHEAP_MODEL if task_kind in CHEAP_KINDS else DEFAULT_MODEL


def gateway(prompt: str, task_kind: str = "generate", system: str | None = None) -> str:
    model = choose_tier(task_kind)
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    resp = chat(messages, model=model)

    usage = resp.usage
    p_in, p_out = PRICES.get(model, (0.0, 0.0))
    cost = (usage.prompt_tokens * p_in + usage.completion_tokens * p_out) / 1_000_000
    _ledger["usd"] += cost
    _ledger["calls"] += 1
    print(f"   [gateway] task={task_kind} -> {model}  ~${cost:.5f}")
    return resp.choices[0].message.content.strip()


if __name__ == "__main__":
    print(gateway("Classify this ticket as billing/order/technical: 'I was charged twice'.",
                  task_kind="classify"))
    print(gateway("Draft a 3-paragraph architecture proposal for a RAG assistant.",
                  task_kind="generate"))
    print(f"\nTotal: {_ledger['calls']} calls, ~${_ledger['usd']:.4f}")
