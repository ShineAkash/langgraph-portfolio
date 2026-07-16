"""08 — Tweet Generator with Evaluate/Optimize Loop.

Generate a tweet, evaluate it with a structured LLM, and either finish
or feed it back for improvement — up to a max number of iterations.
Demonstrates a self-correcting loop with a termination guard.
"""

import operator
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field
from typing import TypedDict, Literal, Annotated

load_dotenv()
generative_model = ChatGroq(model="llama-3.1-8b-instant")
evaluation_model = ChatGroq(model="llama-3.3-70b-versatile")


# Structured evaluator
class TweetEvaluation(BaseModel):
    evaluation: Literal["Approved", "Needs Improvement"] = Field(
        description="Final verdict on the tweet"
    )
    feedback: str = Field(description="Constructive feedback for improvement")
    score: int = Field(description="Score out of 10", ge=0, le=10)


structured_evaluator_llm = evaluation_model.with_structured_output(TweetEvaluation)


# 1. State
class TweetPost(TypedDict):
    topic: str
    tweet: str
    evaluation: Literal["Approved", "Needs Improvement"]
    feedback: str
    score: int
    iteration: int
    max_iterations: int
    tweet_history: Annotated[list[str], operator.add]


# 2. Nodes
def generate_tweet(state: TweetPost) -> TweetPost:
    messages = [
        SystemMessage(content="You are a funny and clever tweet creator."),
        HumanMessage(content=f"Write a short, witty tweet about: {state['topic']}"),
    ]
    tweet = generative_model.invoke(messages).content
    return {"tweet": tweet, "tweet_history": [tweet]}


def evaluate_tweet(state: TweetPost) -> TweetPost:
    messages = [
        SystemMessage(
            content="You are a discerning and insightful tweet evaluator. "
            "Judge the tweet on humour, clarity, and originality."
        ),
        HumanMessage(content=f"Evaluate this tweet: {state['tweet']}"),
    ]
    result = structured_evaluator_llm.invoke(messages)
    return {
        "evaluation": result.evaluation,
        "feedback": result.feedback,
        "score": result.score,
        "iteration": state["iteration"] + 1,
    }


def optimize_tweet(state: TweetPost) -> TweetPost:
    messages = [
        SystemMessage(
            content="You are a skilled and creative tweet reviser. "
            "Take feedback and produce a stronger tweet."
        ),
        HumanMessage(
            content=(
                f"Original tweet: {state['tweet']}\n"
                f"Feedback: {state['feedback']}\n"
                f"Topic: {state['topic']}\n"
                "Write a better version."
            )
        ),
    ]
    new_tweet = generative_model.invoke(messages).content
    return {"tweet": new_tweet, "tweet_history": [new_tweet]}


def route_evaluation(state: TweetPost) -> str:
    if state["evaluation"] == "Approved" or state["iteration"] >= state["max_iterations"]:
        return "Approved"
    return "Needs Improvement"


# 3. Graph
graph = StateGraph(TweetPost)
graph.add_node("generate", generate_tweet)
graph.add_node("evaluate", evaluate_tweet)
graph.add_node("optimize", optimize_tweet)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")
graph.add_conditional_edges(
    "evaluate",
    route_evaluation,
    {"Approved": END, "Needs Improvement": "optimize"},
)
graph.add_edge("optimize", "evaluate")  # the loop

workflow = graph.compile()


if __name__ == "__main__":
    initial_state = {
        "topic": "Indian Railways",
        "iteration": 1,
        "max_iterations": 4,
    }
    final_state = workflow.invoke(initial_state)
    for i, t in enumerate(final_state["tweet_history"], 1):
        print(f"\n--- v{i} ---\n{t}")
    print(f"\nFinal score: {final_state['score']}/10")
