"""04 — Conditional Routing.

Solve a quadratic equation. The discriminant determines which branch
runs: real roots, repeated roots, or no real roots.
Demonstrates `add_conditional_edges` with a routing function.
"""

from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Literal


# 1. State
class QuadState(TypedDict):
    a: int
    b: int
    c: int
    equation: str
    discreminant: int
    result: str


# 2. Nodes
def show_equation(state: QuadState) -> QuadState:
    state["equation"] = f"{state['a']}x^2 + {state['b']}x + {state['c']}"
    return state


def calculate_discreminant(state: QuadState) -> QuadState:
    state["discreminant"] = state["b"] ** 2 - 4 * state["a"] * state["c"]
    return state


def real_roots(state: QuadState) -> QuadState:
    a, b, d = state["a"], state["b"], state["discreminant"]
    root1 = (-b + d ** 0.5) / (2 * a)
    root2 = (-b - d ** 0.5) / (2 * a)
    state["result"] = f"The equation has two real roots: {root1} and {root2}"
    return state


def repeated_roots(state: QuadState) -> QuadState:
    root = -state["b"] / (2 * state["a"])
    state["result"] = f"The equation has a repeated root: {root}"
    return state


def no_real_roots(state: QuadState) -> QuadState:
    state["result"] = "The equation has no real roots"
    return state


# Routing function — maps state to the next node name
def check_condition(state: QuadState) -> Literal["real_roots", "repeated_roots", "no_real_roots"]:
    d = state["discreminant"]
    if d > 0:
        return "real_roots"
    elif d == 0:
        return "repeated_roots"
    return "no_real_roots"


# 3. Graph
graph = StateGraph(QuadState)
graph.add_node("show_equation", show_equation)
graph.add_node("calculate_discreminant", calculate_discreminant)
graph.add_node("real_roots", real_roots)
graph.add_node("repeated_roots", repeated_roots)
graph.add_node("no_real_roots", no_real_roots)

graph.add_edge(START, "show_equation")
graph.add_edge("show_equation", "calculate_discreminant")
graph.add_conditional_edges("calculate_discreminant", check_condition)
graph.add_edge("real_roots", END)
graph.add_edge("repeated_roots", END)
graph.add_edge("no_real_roots", END)

workflow = graph.compile()


if __name__ == "__main__":
    initial_state = {"a": 2, "b": 4, "c": 2}
    final_state = workflow.invoke(initial_state)
    print(final_state)
