"""03 — Prompt Chaining.

Two sequential LLM calls: outline → full blog post. Demonstrates
feeding a downstream node from an upstream node's output via state.
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from typing import TypedDict

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-120b")


# 1. State
class BlogState(TypedDict):
    title: str
    outline: str
    content: str


# 2. Nodes
def generate_outline(state: BlogState) -> BlogState:
    title = state["title"]
    prompt = f"Generate a detailed outline for a blog post on the topic: {title}"
    state["outline"] = model.invoke(prompt).content
    return state


def generate_blog(state: BlogState) -> BlogState:
    title = state["title"]
    outline = state["outline"]
    prompt = f"Write a detailed blog post on the topic: {title} using the following outline: {outline}"
    state["content"] = model.invoke(prompt).content
    return state


# 3. Graph
graph = StateGraph(BlogState)
graph.add_node("generate_outline", generate_outline)
graph.add_node("generate_blog", generate_blog)
graph.add_edge(START, "generate_outline")
graph.add_edge("generate_outline", "generate_blog")
graph.add_edge("generate_blog", END)
workflow = graph.compile()


if __name__ == "__main__":
    initial_state = {"title": "The future of AI in healthcare"}
    final_state = workflow.invoke(initial_state)
    print(final_state["content"])
