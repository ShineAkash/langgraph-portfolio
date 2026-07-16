# 06 — Chatbot with Memory

**What it teaches:** The canonical pattern for any multi-turn LangGraph app.
**Best for:** Real chatbots, agents that need to remember.

## Graph

See [diagram.md](./diagram.md).

## How to run

```bash
python projects/06-chatbot-with-memory/chatbot.py
```

Type to chat, `quit` to exit.

## What you learn

- The `add_messages` reducer — appends messages, replaces by `id`
- `MemorySaver` checkpointer — persists state per `thread_id`
- `config={"configurable": {"thread_id": ...}}` on `invoke()`

## Notebooks

- [`basic_chatbot.ipynb`](./basic_chatbot.ipynb) — original notebook

## Next

→ [07 — Review Triage](../07-review-triage/) (structured output + branching)
