# 04 — Conditional Routing

**What it teaches:** `add_conditional_edges` — one routing function dispatches to N branches.
**Best for:** Anything where the next step depends on runtime state.

## Graph

See [diagram.md](./diagram.md).

## How to run

```bash
python projects/04-conditional-routing/quadratic.py
```

## What you learn

- Writing a routing function with `Literal` return type
- `add_conditional_edges("node", route_fn)` — the canonical branch pattern

## Notebooks

- [`quad_equation.ipynb`](./quad_equation.ipynb) — original notebook

## Next

→ [05 — Parallel Evaluation](../05-parallel-evaluation/) (fan-out)
