"""08 - Orchestrator-Worker

Grok plans a goal into sub-tasks, workers execute them in parallel, and the
orchestrator synthesizes the final answer.  Run:  python 08_orchestrator_worker.py
"""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask


def plan(goal: str) -> list[str]:
    raw = ask(f"Break this goal into 3 independent sub-tasks. Goal: {goal}\n"
              "Return a JSON array of short task strings only.",
              system="Return valid JSON only, no prose.")
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        tasks = json.loads(raw)
        if isinstance(tasks, list):
            return [str(t) for t in tasks][:4]
    except json.JSONDecodeError:
        pass
    return [line.strip("-* ") for line in raw.splitlines() if line.strip()][:4]


def worker(task: str) -> str:
    return ask(f"Complete this sub-task concisely:\n{task}")


def orchestrate(goal: str) -> str:
    tasks = plan(goal)
    print("   [orchestrator] sub-tasks:", tasks)
    with ThreadPoolExecutor(max_workers=max(1, len(tasks))) as pool:
        results = list(pool.map(worker, tasks))
    joined = "\n".join(f"- {t}: {r}" for t, r in zip(tasks, results))
    return ask(f"Synthesize these results into a final answer for the goal '{goal}':\n{joined}")


if __name__ == "__main__":
    print(orchestrate("Produce a launch checklist for a new customer-support chatbot."))
