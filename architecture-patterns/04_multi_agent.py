"""12 - Multi-Agent Collaboration

A coordinator delegates a complex customer issue to specialist agents
(billing, order, technical) and merges their answers into one resolution.
Run:  python 12_multi_agent.py
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask

SPECIALISTS = {
    "billing": "You are a billing specialist. Handle only the billing aspect.",
    "order": "You are an order-management specialist. Handle only the order aspect.",
    "technical": "You are a technical support engineer. Handle only the technical aspect.",
}


def specialist(role: str, issue: str) -> str:
    return ask(f"Customer issue: {issue}\nAddress your part only, concisely.",
               system=SPECIALISTS[role])


def coordinate(issue: str) -> str:
    partials = {role: specialist(role, issue) for role in SPECIALISTS}
    for role, text in partials.items():
        print(f"   [{role}] {text[:70]}...")
    merged = "\n".join(f"{role}: {text}" for role, text in partials.items())
    return ask(f"Combine these specialist responses into one coherent resolution "
               f"for the customer:\n{merged}",
               system="You are the support coordinator. Be clear and friendly.")


if __name__ == "__main__":
    issue = ("I was double-charged for order #12345, it still hasn't shipped, and "
             "the tracking page shows an error.")
    print(coordinate(issue))
