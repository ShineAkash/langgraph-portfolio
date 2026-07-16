"""02 — Simple LLM Question-Answering.

A single-node graph that calls an LLM. Demonstrates the minimal
pattern for wrapping a model call in a LangGraph workflow.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from typing import TypedDict

load_dotenv()

# OpenRouter key is used here (project experiments with multiple providers)
_ = os.getenv("OPENROUTER_API_KEY")
model = ChatGroq(model="openai/gpt-oss-120b")


# 1. State
class LLMState(TypedDict):
    question: str
    answer: str


# 2. Node
def llm_qa(state: LLMState) -> LLMState:
    question = state["question"]
    prompt = f"Answer the following question: {question}"
    state["answer"] = model.invoke(prompt).content
    return state


# 3. Graph
graph = StateGraph(LLMState)
graph.add_node("llm_qa", llm_qa)
graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)
workflow = graph.compile()


if __name__ == "__main__":
    final_state = workflow.invoke({"question": "What is the capital of France?"})
    print(final_state["answer"])
