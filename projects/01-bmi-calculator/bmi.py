"""01 — BMI Calculator (first LangGraph).

A two-node pipeline: compute BMI, then label it. Demonstrates the
minimal `StateGraph` pattern — no LLM, just pure Python state.
"""

from langgraph.graph import START, END, StateGraph
from typing import TypedDict


# 1. State
class BMIState(TypedDict):
    height_m: float  # metres
    weight_kg: float  # kilograms
    bmi: float
    catagory: str


# 2. Nodes
def calculate_bmi(state: BMIState) -> BMIState:
    height = state["height_m"]
    weight = state["weight_kg"]
    bmi_value = weight / (height ** 2)
    state["bmi"] = round(bmi_value, 2)
    return state


def label_bmi(state: BMIState) -> BMIState:
    bmi = state["bmi"]
    if bmi < 18.5:
        state["catagory"] = "Underweight"
    elif 18.5 <= bmi < 25:
        state["catagory"] = "Normal"
    elif 25 <= bmi < 30:
        state["catagory"] = "Overweight"
    else:
        state["catagory"] = "Obese"
    return state


# 3. Graph
graph = StateGraph(BMIState)
graph.add_node("calculate_bmi", calculate_bmi)
graph.add_node("label_bmi", label_bmi)
graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", "label_bmi")
graph.add_edge("label_bmi", END)
workflow = graph.compile()


if __name__ == "__main__":
    result = workflow.invoke({"height_m": 1.75, "weight_kg": 70})
    print(result)
