"""07 - Router / Handoff

Grok classifies the request intent, then hands off to the matching specialist
agent.  Run:  python 07_router_handoff.py
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask


def classify(request: str) -> str:
    label = ask(request, system="Classify the request as exactly one of: "
                                "billing, order, technical. Reply with one word only.")
    label = label.lower().strip().strip(".")
    return label if label in {"billing", "order", "technical"} else "technical"


def billing_agent(r: str) -> str:
    return ask(r, system="You are a billing specialist. Be helpful and concise.")


def order_agent(r: str) -> str:
    return ask(r, system="You are an order-management specialist. Be concise.")


def technical_agent(r: str) -> str:
    return ask(r, system="You are a technical support engineer. Be concise.")


HANDOFF = {"billing": billing_agent, "order": order_agent, "technical": technical_agent}


def route(request: str) -> str:
    label = classify(request)
    print(f"   [router] -> {label}")
    return HANDOFF[label](request)


if __name__ == "__main__":
    for r in ["I was charged twice this month.",
              "Where is my package? Order #12345.",
              "The app crashes when I upload a file."]:
        print("Q:", r)
        print("A:", route(r), "\n")
