"""09 - Evaluator-Optimizer

Generate an answer, check it against an objective bar, and loop until it passes.
Here Grok writes SQL; a real database execution is the evaluator.
Run:  python 09_evaluator_optimizer.py
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask


def build_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.executescript(
        "CREATE TABLE orders(id INTEGER, customer TEXT, amount REAL, status TEXT);"
        "INSERT INTO orders VALUES (1,'Acme',120.0,'paid'),(2,'Acme',80.0,'refunded'),"
        "(3,'Globex',200.0,'paid'),(4,'Globex',50.0,'paid');"
    )
    return con


def generate_sql(question: str, feedback: str | None = None) -> str:
    prompt = (f"Schema: orders(id, customer, amount, status).\n"
              f"Write a single SQLite query to answer: {question}\n"
              "Return ONLY the SQL, no markdown.")
    if feedback:
        prompt += f"\nThe previous attempt failed with: {feedback}\nFix it."
    sql = ask(prompt, system="Return only valid SQLite SQL.")
    return sql.strip().strip("`").replace("sql\n", "").strip()


def optimize(question: str, max_rounds: int = 3):
    con = build_db()
    feedback = None
    sql = ""
    for i in range(1, max_rounds + 1):
        sql = generate_sql(question, feedback)
        print(f"   [attempt {i}] {sql}")
        try:
            rows = con.execute(sql).fetchall()
            if rows:  # objective pass condition: query runs AND returns rows
                return sql, rows
            feedback = "query executed but returned no rows"
        except sqlite3.Error as e:
            feedback = f"SQL error: {e}"
        print(f"   [evaluator] fail -> {feedback}")
    return sql, None


if __name__ == "__main__":
    sql, rows = optimize("total paid amount per customer")
    print("FINAL SQL:", sql)
    print("ROWS:", rows)
