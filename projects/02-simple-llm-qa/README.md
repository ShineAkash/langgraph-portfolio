# 02 — Simple LLM Q&A

**What it teaches:** A single-node graph wrapping one LLM call.
**Best for:** The "ask the model" baseline before adding any control flow.

## Graph

See [diagram.md](./diagram.md).

## How to run

```bash
python projects/02-simple-llm-qa/simple_llm.py
```

Requires `OPENROUTER_API_KEY` in `.env`.

## What you learn

- Wiring an LLM provider (`ChatGroq` against OpenRouter)
- Returning state updates from a node
- When LangGraph is overkill — and when it isn't

## Notebooks

- [`simple_llm_workflow.ipynb`](./simple_llm_workflow.ipynb) — original notebook

## Next

→ [03 — Prompt Chaining](../03-prompt-chaining/) (sequential composition)
