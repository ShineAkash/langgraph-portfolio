"""06 — Chatbot with Memory.

A stateful chatbot using `add_messages` reducer and `MemorySaver`
checkpointing. Demonstrates the standard pattern for any
multi-turn LangGraph application.
"""

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant")


# 1. State — `add_messages` is the canonical message reducer
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 2. Node
def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


# 3. Graph with checkpointer for conversation memory
checkpointer = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    thread_id = "1"
    config = {"configurable": {"thread_id": thread_id}}
    while True:
        user_message = input("User: ").strip()
        if user_message.lower() in {"quit", "exit"}:
            break
        response = chatbot.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
        )
        print("Assistant:", response["messages"][-1].content)
