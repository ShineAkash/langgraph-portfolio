# 09 — UPSC Essay Evaluator ⭐

**The flagship.** Three LLM evaluators (language, analysis, clarity) run **in parallel**, each emitting a structured score. A final aggregator combines the feedback and computes the average.

This is the same shape as a production multi-agent evaluator (LLM-as-a-judge, Constitutional AI, etc.): many specialised critics, then aggregate.

## Graph

See [diagram.md](./diagram.md).

## Live demo

The Streamlit demo lives at `demos/upsc_essay_app.py` — see the
[demos README](../../demos/README.md) for run / deploy instructions.

## How to run

```bash
python projects/09-upsc-essay-evaluator/upsc_essay.py
```

## What you learn

- **Fan-out**: three `START → evaluator` edges run the three nodes concurrently
- **`operator.add` reducer**: scores merge into `individual_scores: list[float]`
- **Fan-in**: all three evaluators feed a single aggregator
- **Structured output everywhere** — every evaluator returns a Pydantic-validated `EvalutationSchema`
- The pattern generalises to *any* "many-critics-one-aggregator" problem

## Notebooks

- [`upsc_essay_workflow.ipynb`](./upsc_essay_workflow.ipynb) — original notebook

## Patterns used

| Pattern | Where |
|---|---|
| `StateGraph` | `UPSCState` typed state |
| Parallel edges | 3× `START → evaluator` |
| `operator.add` reducer | `individual_scores: Annotated[list[float], operator.add]` |
| Structured output | `model.with_structured_output(EvalutationSchema)` |
| Fan-in | 3× `evaluator → final_evaluation` |
