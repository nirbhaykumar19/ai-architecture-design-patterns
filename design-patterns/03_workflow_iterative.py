"""06 - Workflow: Iterative Refinement

Loop draft -> critique -> improve until a quality bar is met.
Run:  python 06_workflow_iterative.py
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask


def iterative(topic: str, rounds: int = 2) -> str:
    draft = ask(f"Write a one-paragraph summary of: {topic}")
    for i in range(1, rounds + 1):
        critique = ask(f"Critique this draft in 2 bullet points:\n{draft}")
        print(f"   [round {i}] critique: {critique[:80]}...")
        draft = ask(f"Improve the draft using the critique.\nDraft:\n{draft}\nCritique:\n{critique}")
    return draft


if __name__ == "__main__":
    print(iterative("retrieval-augmented generation"))
