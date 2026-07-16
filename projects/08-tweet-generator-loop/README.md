# 08 — Tweet Generator with Optimize Loop

**What it teaches:** A self-correcting loop — generate, evaluate, optimize, repeat.
**Best for:** Iterative refinement with a hard stop.

## Graph

See [diagram.md](./diagram.md).

## How to run

```bash
python projects/08-tweet-generator-loop/tweet_loop.py
```

## What you learn

- A loop edge: `optimize → evaluate` (cycles back)
- Termination guards — `max_iterations` and explicit verdict
- `operator.add` reducer to collect the iteration history
- Why "self-critique" agents are just `generate → evaluate → optimize` loops

## Notebooks

- [`tweet_post_gen.ipynb`](./tweet_post_gen.ipynb) — original notebook

## Next

→ [09 — UPSC Essay Evaluator](../09-upsc-essay-evaluator/) (parallel evaluators + aggregation)
