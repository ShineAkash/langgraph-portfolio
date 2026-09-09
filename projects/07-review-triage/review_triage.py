"""07 — Review Triage.

Classify a product review by sentiment, then either draft a positive
reply or run a deeper diagnosis and write a negative reply.
Demonstrates Pydantic-based structured output and a 2-way branch.
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field
from typing import TypedDict, Literal

load_dotenv()
model = ChatGroq(model=os.environ["GROQ_MODEL"])


# Structured output schemas
class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="The sentiment of the review"
    )


class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(
        description="The issue type of the review"
    )
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(
        description="The emotional tone of the review"
    )
    urgency: Literal["low", "medium", "high"] = Field(
        description="How urgent the issue is"
    )


structured_model = model.with_structured_output(SentimentSchema)
structured_model2 = model.with_structured_output(DiagnosisSchema)


# 1. State
class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict
    response: str


# 2. Nodes
def find_sentiment(state: ReviewState) -> ReviewState:
    prompt = (
        f"What is the sentiment of the following review? "
        f"Review: {state['review']}"
    )
    result = structured_model.invoke(prompt)
    return {"sentiment": result.sentiment}


def positive_response(state: ReviewState) -> ReviewState:
    prompt = (
        f"Write a warm thank-you reply to this positive review: {state['review']}"
    )
    state["response"] = model.invoke(prompt).content
    return state


def run_diagnosis(state: ReviewState) -> ReviewState:
    prompt = (
        f"Diagnose the following negative review. Identify the issue type, "
        f"tone, and urgency. Review: {state['review']}"
    )
    result = structured_model2.invoke(prompt)
    return {"diagnosis": result.model_dump()}


def negaitive_response(state: ReviewState) -> ReviewState:
    diagnosis = state["diagnosis"]
    prompt = (
        f"You are a customer-support agent. The review was negative. "
        f"Diagnosis: {diagnosis}. Draft an empathetic reply that addresses "
        f"the issue: {state['review']}"
    )
    state["response"] = model.invoke(prompt).content
    return state


def check_sentiment(state: ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    return "positive_response" if state["sentiment"] == "positive" else "run_diagnosis"


# 3. Graph
graph = StateGraph(ReviewState)
graph.add_node("find_sentiment", find_sentiment)
graph.add_node("positive_response", positive_response)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negaitive_response)

graph.add_edge(START, "find_sentiment")
graph.add_conditional_edges("find_sentiment", check_sentiment)
graph.add_edge("run_diagnosis", "negative_response")
graph.add_edge("positive_response", END)
graph.add_edge("negative_response", END)

workflow = graph.compile()


if __name__ == "__main__":
    initial_state = {
        "review": (
            "I am really disappointed with this service. The app keeps crashing "
            "and no one from support has responded to my tickets."
        )
    }
    final_state = workflow.invoke(initial_state)
    print(final_state)
