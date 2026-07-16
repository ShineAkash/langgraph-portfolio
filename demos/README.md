# Live Demos

## `upsc_essay_app.py` — UPSC Essay Evaluator

**🚀 [upsc-essay-evaluatorr.streamlit.app](https://upsc-essay-evaluatorr.streamlit.app/)**

A Streamlit app wrapping the [UPSC essay evaluator](../projects/09-upsc-essay-evaluator/).

Three LLM evaluators (language, analysis, clarity of thought) run in
parallel. Scores are merged with `operator.add`, then a final node
aggregates the feedback.

### Run locally

```bash
pip install -r requirements.txt
streamlit run demos/upsc_essay_app.py
```

Open http://localhost:8501 in your browser.

You'll need `GROQ_API_KEY` in your `.env` (see `.env.example`).

### Deploy to Streamlit Cloud (free, ~2 min)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Point it at `demos/upsc_essay_app.py`.
4. In **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_..."
   ```
5. Click **Deploy**. Share the URL it gives you.

### Features

- Side-by-side comparison of all 3 evaluators
- The Mermaid graph is rendered inline
- A "Load sample" button for the included sample essay
- Metric cards with the average + per-evaluator scores
