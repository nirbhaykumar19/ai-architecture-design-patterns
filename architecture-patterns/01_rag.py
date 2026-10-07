"""01 - RAG (Retrieval-Augmented Generation)

Retrieve relevant private context, then ask GPT to answer ONLY from it with
citations. Run:  python 01_rag.py
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import ask
from knowledge_base import retrieve


def rag_answer(question: str):
    docs = retrieve(question)
    context = "\n".join(f"[{doc_id}] {text}" for doc_id, text in docs)
    system = (
        "You are a grounded assistant. Answer ONLY from the provided context and "
        "cite the source id in square brackets. If the answer is not in the "
        "context, say you do not have that information."
    )
    return ask(f"Context:\n{context}\n\nQuestion: {question}", system=system), docs


if __name__ == "__main__":
    for q in ["What is our 2026 parental-leave policy?",
              "How long do UK customers have to return faulty goods?"]:
        answer, docs = rag_answer(q)
        print("Q:", q)
        print("Retrieved:", [d[0] for d in docs])
        print("A:", answer, "\n")
