"""Streamlit demo for the UPSC Essay Evaluator.

Run locally:
    streamlit run demos/upsc_essay_app.py

Deploy:
    Push to GitHub → https://share.streamlit.io → "New app" → pick this repo.
    Add GROQ_API_KEY and GROQ_MODEL under "Secrets" (advanced settings).
    Done — share the URL.
"""

import os
import operator
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing import Annotated, TypedDict

# Page config
st.set_page_config(
    page_title="UPSC Essay Evaluator",
    page_icon="📝",
    layout="wide",
)

# Load GROQ_API_KEY from Streamlit secrets (cloud) or .env (local).
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["GROQ_MODEL"] = st.secrets["GROQ_MODEL"]
except Exception:  # noqa: BLE001 — local dev, no secrets.toml
    load_dotenv()

# ---------- Model + structured output ----------
class EvalutationSchema(BaseModel):
    feedback: str = Field(description="Detailed feedback for the essay")
    score: float = Field(description="The score out of 10", ge=0, le=10)


def _build_structured_model(model_name: str):
    """Build a structured-output model for a given Groq model name."""
    return ChatGroq(model=model_name).with_structured_output(EvalutationSchema)


# Ordered fallback list. Add optional comma-separated fallback model IDs through
# GROQ_FALLBACK_MODELS; the primary model comes from GROQ_MODEL.
_MODEL_CHAIN = (os.environ["GROQ_MODEL"],) + tuple(
    model.strip()
    for model in os.getenv("GROQ_FALLBACK_MODELS", "").split(",")
    if model.strip()
)


def _invoke_with_fallback(prompt: str) -> EvalutationSchema:
    last_err = None
    for name in _MODEL_CHAIN:
        try:
            return _build_structured_model(name).invoke(prompt)
        except Exception as e:  # noqa: BLE001 — we want to catch any groq error
            last_err = e
    raise last_err  # type: ignore[misc]


# ---------- State + node functions ----------
class UPSCState(TypedDict):
    essay: str
    language_feedback: str
    clarity_feedback: str
    analysis_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[float], operator.add]
    avg_score: float


def evaluate_language(state: UPSCState) -> UPSCState:
    prompt = (
        "Evaluate the language and grammar of the following essay and "
        f"provide feedback and assign a score out of 10.\n {state['essay']}"
    )
    result = _invoke_with_fallback(prompt)
    return {"language_feedback": result.feedback, "individual_scores": [result.score]}


def evaluate_analysis(state: UPSCState) -> UPSCState:
    prompt = (
        "Evaluate the depth of analysis of the following essay and "
        f"provide feedback and assign a score out of 10.\n {state['essay']}"
    )
    result = _invoke_with_fallback(prompt)
    return {"analysis_feedback": result.feedback, "individual_scores": [result.score]}


def evaluate_thought(state: UPSCState) -> UPSCState:
    prompt = (
        "Evaluate the clarity of thought of the following essay and "
        f"provide feedback and assign a score out of 10.\n {state['essay']}"
    )
    result = _invoke_with_fallback(prompt)
    return {"clarity_feedback": result.feedback, "individual_scores": [result.score]}


def final_evaluation(state: UPSCState) -> UPSCState:
    # Aggregator doesn't need structured output — use the primary model directly
    primary = ChatGroq(model=_MODEL_CHAIN[0])
    prompt = (
        "Based on the following feedbacks, provide a summarized feedback "
        f"for the essay:\n"
        f"Language Feedback: {state['language_feedback']}\n"
        f"Analysis Feedback: {state['analysis_feedback']}\n"
        f"Clarity Feedback: {state['clarity_feedback']}"
    )
    overall_feedback = primary.invoke(prompt).content
    avg_score = sum(state["individual_scores"]) / len(state["individual_scores"])
    return {"overall_feedback": overall_feedback, "avg_score": avg_score}


# ---------- Graph ----------
@st.cache_resource
def build_graph():
    graph = StateGraph(UPSCState)
    graph.add_node("evaluate_language", evaluate_language)
    graph.add_node("evaluate_analysis", evaluate_analysis)
    graph.add_node("evaluate_thought", evaluate_thought)
    graph.add_node("final_evaluation", final_evaluation)

    # Fan-out
    graph.add_edge(START, "evaluate_language")
    graph.add_edge(START, "evaluate_analysis")
    graph.add_edge(START, "evaluate_thought")

    # Fan-in
    graph.add_edge("evaluate_language", "final_evaluation")
    graph.add_edge("evaluate_analysis", "final_evaluation")
    graph.add_edge("evaluate_thought", "final_evaluation")
    graph.add_edge("final_evaluation", END)

    return graph.compile()


workflow = build_graph()


# ---------- UI ----------
SAMPLE_ESSAY = """Artificial Intelligence (AI) is rapidly transforming the world, and India is
emerging as one of the key players in this technological revolution. AI refers
to machines and systems that can perform tasks requiring human intelligence,
such as learning, reasoning, problem-solving, and decision-making.

One of the most important roles of AI in India is in economic development and
industry. AI is being widely adopted in sectors such as information technology,
manufacturing, finance, and e-commerce. Startups and large companies use AI
for automation, data analysis, fraud detection, customer support chatbots, and
personalized services.

AI is also making a strong impact on healthcare in India. AI-powered tools help
doctors in early disease detection, medical imaging, diagnosis, and treatment
planning. In rural and remote areas, AI-based telemedicine and virtual health
assistants improve access to quality healthcare.

In conclusion, AI has a transformative role in India's development. When used
responsibly, AI can accelerate economic growth, improve quality of life, and
help India become a global technology leader."""


st.title("📝 UPSC Essay Evaluator")
st.caption(
    "Three LLM evaluators run **in parallel** to score an essay on language, "
    "analysis, and clarity of thought. A final aggregator synthesises feedback."
)

with st.expander("🕸️ View the graph"):
    st.markdown(
        """
```mermaid
graph TD
    START([START]) --> A[evaluate_language]
    START --> B[evaluate_analysis]
    START --> C[evaluate_thought]
    A --> D[final_evaluation]
    B --> D
    C --> D
    D --> END([END])
```
"""
    )

col_input, col_run = st.columns([4, 1])
with col_input:
    essay = st.text_area("Your essay", value=SAMPLE_ESSAY, height=300)
with col_run:
    st.write("")
    st.write("")
    run_clicked = st.button("▶ Evaluate", type="primary", use_container_width=True)
    sample_clicked = st.button("Load sample", use_container_width=True)

if sample_clicked:
    st.rerun()  # text_area is already populated; this just re-renders

if run_clicked:
    if not essay.strip():
        st.error("Please paste an essay first.")
    else:
        with st.spinner("Running three parallel evaluators..."):
            try:
                result = workflow.invoke({"essay": essay})
            except Exception as e:
                st.error(f"Workflow failed: {e}")
                st.stop()

        # Top: score header
        st.divider()
        score = result.get("avg_score", 0)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("⭐ Average score", f"{score:.2f} / 10")
        m2.metric("Language", f"{result['individual_scores'][0]:.1f}")
        m3.metric("Analysis", f"{result['individual_scores'][1]:.1f}")
        m4.metric("Clarity of thought", f"{result['individual_scores'][2]:.1f}")

        st.divider()

        # 4 panels
        a, b, c, d = st.columns(4)
        with a:
            st.subheader("📖 Language")
            st.write(result["language_feedback"])
        with b:
            st.subheader("🔍 Analysis")
            st.write(result["analysis_feedback"])
        with c:
            st.subheader("💡 Clarity of thought")
            st.write(result["clarity_feedback"])
        with d:
            st.subheader("✨ Overall")
            st.write(result["overall_feedback"])
