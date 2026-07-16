# 07 — Review Triage

**What it teaches:** Pydantic structured output + 2-way conditional branch.
**Best for:** Classify-then-act workflows, support routing.

## Graph

See [diagram.md](./diagram.md).

## How to run

```bash
python projects/07-review-triage/review_triage.py
```

## What you learn

- `model.with_structured_output(PydanticSchema)` for typed LLM responses
- A second LLM call for the harder (negative) branch — diagnosis before response
- Routing on a `Literal` state field

## Notebooks

- [`review_reply_workflow.ipynb`](./review_reply_workflow.ipynb) — original notebook

## Next

→ [08 — Tweet Generator Loop](../08-tweet-generator-loop/) (loops with termination)
