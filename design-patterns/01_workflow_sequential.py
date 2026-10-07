"""04 - Workflow: Sequential

A fixed chain where each step consumes the previous step's output.
Run:  python 04_workflow_sequential.py
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask


def sequential(feature: str) -> str:
    analysis = ask(f"List 3 key requirements for: {feature}", system="Be concise, use bullets.")
    design = ask(f"Propose a short design given these requirements:\n{analysis}")
    tests = ask(f"Write 3 test cases for this design:\n{design}")
    return f"REQUIREMENTS\n{analysis}\n\nDESIGN\n{design}\n\nTESTS\n{tests}"


if __name__ == "__main__":
    print(sequential("a password reset feature"))
