"""05 — Parallel Evaluation (Batsman stats).

Three metrics (strike rate, balls per boundary, boundary %) are computed
in parallel and merged into one summary. Demonstrates a custom reducer
(`replace_value`) and fan-out / fan-in via multiple START edges.
"""

from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Annotated


# A custom reducer: only overwrite when the new value is non-None.
def replace_value(current, new):
    return new if new is not None else current


# 1. State
class BatsmanState(TypedDict):
    runs: Annotated[int, replace_value]
    balls: Annotated[int, replace_value]
    fours: Annotated[int, replace_value]
    sixes: Annotated[int, replace_value]
    sr: float
    bpb: float
    boundry_precent: float
    summary: str


# 2. Nodes
def calculate_sr(state: BatsmanState) -> BatsmanState:
    sr = (state["runs"] / state["balls"]) * 100
    return {"sr": sr}


def calculate_bpb(state: BatsmanState) -> BatsmanState:
    bpb = state["balls"] / (state["fours"] + state["sixes"])
    return {"bpb": bpb}


def calculate_boundry_precent(state: BatsmanState) -> BatsmanState:
    boundry_precent = (((state["fours"] * 4) + (state["sixes"] * 6)) / state["runs"]) * 100
    return {"boundry_precent": boundry_precent}


def summary(state: BatsmanState) -> BatsmanState:
    state["summary"] = (
        f"Strikes Rate: {state['sr']} \n"
        f"Balls per boundary: {state['bpb']} \n"
        f"Boundary percent: {state['boundry_precent']} \n"
    )
    return state


# 3. Graph
graph = StateGraph(BatsmanState)
graph.add_node("calculate_sr", calculate_sr)
graph.add_node("calculate_bpb", calculate_bpb)
graph.add_node("calculate_boundry_precent", calculate_boundry_precent)
graph.add_node("summary", summary)

# Fan-out: START connects to all three metric nodes
graph.add_edge(START, "calculate_sr")
graph.add_edge(START, "calculate_bpb")
graph.add_edge(START, "calculate_boundry_precent")

# Fan-in: all three feed into summary
graph.add_edge("calculate_sr", "summary")
graph.add_edge("calculate_bpb", "summary")
graph.add_edge("calculate_boundry_precent", "summary")
graph.add_edge("summary", END)

workflow = graph.compile()


if __name__ == "__main__":
    initial_state = {"runs": 100, "balls": 50, "fours": 6, "sixes": 4}
    final_state = workflow.invoke(initial_state)
    print(final_state["summary"])
