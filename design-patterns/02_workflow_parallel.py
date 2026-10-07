"""05 - Workflow: Parallel / Concurrent

Independent sub-tasks run at the same time, then an aggregator merges the
results.  Run:  python 05_workflow_parallel.py
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask


def parallel(incident: str) -> str:
    angles = {
        "logs": f"From application logs, what likely caused: {incident}?",
        "metrics": f"From metrics/latency, what likely caused: {incident}?",
        "traces": f"From distributed traces, what likely caused: {incident}?",
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        findings = dict(zip(angles, pool.map(
            lambda p: ask(p, system="Answer in one sentence."), angles.values())))
    return ask("Aggregate these findings into a single root-cause hypothesis:\n" +
               "\n".join(f"{k}: {v}" for k, v in findings.items()))


if __name__ == "__main__":
    print(parallel("checkout latency spiked to 5s"))
