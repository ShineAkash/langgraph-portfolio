# 05 — Parallel Evaluation (Batsman Stats)

**What it teaches:** Fan-out + fan-in via multiple `START → node` edges, with a custom reducer.
**Best for:** Computing many metrics at once and aggregating.

## Graph

See [diagram.md](./diagram.md).

## How to run

```bash
python projects/05-parallel-evaluation/batsman.py
```

## What you learn

- Multiple edges from `START` run their target nodes concurrently
- A custom `replace_value` reducer (overwrite only on non-None) for safe partial updates
- Fan-in via multiple nodes → one aggregator

## Notebooks

- [`batsman_workflow.ipynb`](./batsman_workflow.ipynb) — original notebook

## Next

→ [06 — Chatbot with Memory](../06-chatbot-with-memory/) (state, but for messages)
