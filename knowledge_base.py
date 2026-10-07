"""Knowledge base for the RAG demos: loads docs/*.txt and provides retrieval.

Uses a dependency-free lexical retriever so the demos run without an embeddings
service. In production, replace `retrieve` with a vector search (e.g. Chroma,
pgvector, Qdrant) over embedded chunks.
"""
from __future__ import annotations

import os
import re
from difflib import SequenceMatcher

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")


def load_kb() -> list[tuple[str, str]]:
    """Return a list of (doc_id, text) loaded from every .txt file in docs/."""
    kb: list[tuple[str, str]] = []
    for name in sorted(os.listdir(DOCS_DIR)):
        if name.endswith(".txt"):
            with open(os.path.join(DOCS_DIR, name), encoding="utf-8") as f:
                kb.append((os.path.splitext(name)[0], f.read().strip()))
    return kb


KB = load_kb()


def retrieve(query: str, k: int = 2) -> list[tuple[str, str]]:
    """Return the top-k (doc_id, text) passages most relevant to the query."""
    def score(text: str) -> float:
        q = set(re.findall(r"\w+", query.lower()))
        d = set(re.findall(r"\w+", text.lower()))
        overlap = len(q & d) / (len(q) + 1)
        fuzzy = SequenceMatcher(None, query.lower(), text.lower()).ratio()
        return overlap + 0.3 * fuzzy

    return sorted(KB, key=lambda doc: score(doc[1]), reverse=True)[:k]


if __name__ == "__main__":
    print(f"Loaded {len(KB)} documents: {[doc_id for doc_id, _ in KB]}")
    print("Top match for 'uk refund':", retrieve("uk refund", k=1)[0][0])
