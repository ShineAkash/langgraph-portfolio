# 01 — BMI Calculator

**What it teaches:** The minimal `StateGraph` — two pure-Python nodes, no LLM.
**Best for:** A 30-second tour of the API.

## Graph

See [diagram.md](./diagram.md).

## How to run

```bash
python projects/01-bmi-calculator/bmi.py
```

## What you learn

- Defining a `TypedDict` state
- `add_node`, `add_edge`, `START`, `END`
- `workflow.compile()` and `workflow.invoke()`

## Notebooks

- [`bmi_calculator.ipynb`](./bmi_calculator.ipynb) — original notebook

## Next

→ [02 — Simple LLM Q&A](../02-simple-llm-qa/) (add an LLM call)
