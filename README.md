# AI Architecture & Design Patterns — runnable demos with Grok (xAI)

Minimal, dependency-light Python examples that demonstrate each pattern from the
*AI Architecture & Design Patterns* deck, powered by **Grok** via the
OpenAI-compatible xAI API.

## Project layout

```
grok_patterns/
├── docs/                         # sample private corpus used by the RAG demos
│   ├── hr_policy.txt
│   ├── refund_policy_eu.txt
│   ├── refund_policy_uk.txt
│   └── security_policy.txt
├── common.py                     # shared Grok client (get_client, chat, ask)
├── knowledge_base.py             # loads docs/ + lexical retrieve() for RAG
├── tools.py                      # simulated enterprise tools for the ReAct demo
├── 01_rag.py                     # Retrieval-Augmented Generation
├── 02_agentic_rag.py            # agent decides when/what to retrieve (tool calls)
├── 03_ai_gateway.py             # tiered model routing + cost ledger
├── 04_workflow_sequential.py    # fixed step-by-step chain
├── 05_workflow_parallel.py      # concurrent sub-tasks + aggregation
├── 06_workflow_iterative.py     # draft → critique → improve loop
├── 07_router_handoff.py         # classify intent → specialist agent
├── 08_orchestrator_worker.py    # plan → delegate → synthesize
├── 09_evaluator_optimizer.py    # generate → objective check → fix loop (SQL)
├── 10_react_tool_use.py         # reason + act + observe with function calling
├── 11_human_in_the_loop.py      # AI recommends, human approves before execute
├── 12_multi_agent.py            # coordinator + specialist agents collaborate
├── run_all.py                   # run every demo in order
└── requirements.txt
```

## Setup

1. **Get an API key** at <https://console.x.ai>.
2. **Set the key** as an environment variable:

   ```powershell
   # Windows PowerShell (open a NEW terminal afterwards)
   setx XAI_API_KEY "xai-..."
   ```
   ```bash
   # macOS / Linux
   export XAI_API_KEY="xai-..."
   ```
3. **Install the dependency**:

   ```bash
   pip install -r requirements.txt
   ```

Optional model overrides:

```bash
set GROK_MODEL=grok-4            # default / frontier tier
set GROK_CHEAP_MODEL=grok-3-mini # cheap tier for classify/route
```

## Run

```bash
python 01_rag.py          # run one pattern
python run_all.py         # run them all in order
```

## Pattern → file map

| Pattern | File |
|---|---|
| RAG | `01_rag.py` |
| Agentic RAG | `02_agentic_rag.py` |
| AI Gateway | `03_ai_gateway.py` |
| Sequential workflow | `04_workflow_sequential.py` |
| Parallel / concurrent | `05_workflow_parallel.py` |
| Iterative refinement | `06_workflow_iterative.py` |
| Router / Handoff | `07_router_handoff.py` |
| Orchestrator-Worker | `08_orchestrator_worker.py` |
| Evaluator-Optimizer | `09_evaluator_optimizer.py` |
| ReAct (tool use) | `10_react_tool_use.py` |
| Human-in-the-Loop | `11_human_in_the_loop.py` |
| Multi-agent collaboration | `12_multi_agent.py` |

> The demos use a lexical retriever and in-memory data so they run without extra
> services. In production, swap `knowledge_base.retrieve` for a vector search and
> replace the simulated tools in `tools.py` with real APIs.
