"""11 - Human-in-the-Loop

The AI recommends a high-impact action; a human must approve before it executes.
Run:  python 11_human_in_the_loop.py
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask


def recommend(incident: str) -> str:
    return ask(f"A production incident occurred: {incident}\n"
               "Recommend ONE specific remediation action in one sentence.",
               system="Be specific and conservative.")


def execute(action: str) -> None:
    print(f"   [executed] {action}")


def handle(incident: str, auto_approve: bool | None = None) -> str:
    action = recommend(incident)
    print(f"AI recommends: {action}")
    if auto_approve is None:
        decision = input("Approve this action? [y/N] ").strip().lower()
    else:
        decision = "y" if auto_approve else "n"
    if decision == "y":
        execute(action)
        return "approved"
    print("   [skipped] human rejected the action")
    return "rejected"


if __name__ == "__main__":
    # auto_approve=False keeps this demo non-interactive & safe.
    # Set auto_approve=None for a real interactive y/N prompt.
    handle("payment service returning 500s for 5 minutes", auto_approve=False)
