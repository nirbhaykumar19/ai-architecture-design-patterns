"""Shared OpenAI client and helpers for the AI design-pattern demos.

Setup
-----
1. Get an API key at https://platform.openai.com/api-keys
2. Set it as an environment variable:

       setx OPENAI_API_KEY "sk-..."       # Windows (open a NEW terminal after)
       export OPENAI_API_KEY="sk-..."     # macOS / Linux

3. (optional) choose models:

       set OPENAI_MODEL=gpt-4o             # default / frontier tier
       set OPENAI_CHEAP_MODEL=gpt-4o-mini  # cheap tier for classify/route
"""
from __future__ import annotations

import os
import time

from openai import OpenAI

DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
CHEAP_MODEL = os.environ.get("OPENAI_CHEAP_MODEL", "gpt-4o-mini")

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Return a cached OpenAI client configured for the OpenAI endpoint."""
    global _client
    if _client is None:
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Get a key at https://platform.openai.com/api-keys and set it, e.g.\n"
                '  setx OPENAI_API_KEY "sk-..."   (Windows, then open a new terminal)\n'
                '  export OPENAI_API_KEY="sk-..." (macOS/Linux)'
            )
        _client = OpenAI(api_key=key)
    return _client


def chat(messages, model=None, tools=None, tool_choice=None, temperature=0.2, **kw):
    """Call chat.completions and print simple token-usage telemetry."""
    client = get_client()
    model = model or DEFAULT_MODEL
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
        temperature=temperature,
        **kw,
    )
    usage = getattr(resp, "usage", None)
    if usage:
        print(f"   [gpt] model={model} in={usage.prompt_tokens} "
              f"out={usage.completion_tokens} {time.time() - t0:.1f}s")
    return resp


def ask(prompt, system=None, model=None, temperature=0.2) -> str:
    """One-shot convenience helper: send a prompt, return the text answer."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return chat(messages, model=model, temperature=temperature).choices[0].message.content.strip()
