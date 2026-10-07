"""Simulated enterprise tools used by the ReAct demo (10_react_tool_use.py).

Each function stands in for a real API (order service, payment service). The
TOOLS_SCHEMA list is the OpenAI-compatible function schema Grok uses to decide
which tool to call; TOOLS_IMPL maps tool names back to the Python callables.
"""
from __future__ import annotations

ORDERS = {"12345": {"status": "failed", "reason": "payment_declined"}}
PAYMENTS = {"12345": {"code": "card_expired", "retryable": True}}


def get_order_status(order_id: str) -> dict:
    """Return the status of an order by id."""
    return ORDERS.get(order_id, {"status": "unknown"})


def get_payment_log(order_id: str) -> dict:
    """Return the payment log for an order by id."""
    return PAYMENTS.get(order_id, {"code": "none"})


TOOLS_IMPL = {
    "get_order_status": get_order_status,
    "get_payment_log": get_payment_log,
}

TOOLS_SCHEMA = [
    {"type": "function", "function": {
        "name": "get_order_status",
        "description": "Get the status of an order by id.",
        "parameters": {"type": "object",
                       "properties": {"order_id": {"type": "string"}},
                       "required": ["order_id"]}}},
    {"type": "function", "function": {
        "name": "get_payment_log",
        "description": "Get the payment log for an order by id.",
        "parameters": {"type": "object",
                       "properties": {"order_id": {"type": "string"}},
                       "required": ["order_id"]}}},
]
