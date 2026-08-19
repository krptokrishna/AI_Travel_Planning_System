'''
# pip install langgraph langchain langchain-openai langchain-groq langchain-community langchain-tavily psycopg[binary] psycopg_pool python-dotenv tavily-python pip install requests streamlit

# install PostgresSql and create database
CREATE DATABASE langgraph_memory;  ( or open pgadmin4 and create database there )
'''
# LangGraph Multi-Agent Travel Booking System with Long-Term Memory

# main.py

import os
from typing import TypedDict, Annotated
import operator

import psycopg
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import interrupt, Command
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)
# State
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    human_approval: str
    booking_status: str
    booking_confirmation: str

# Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content=f"Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
def human_approval(state: TravelState):
    decision = interrupt({
        "type": "booking_approval",
        "message": "Please review the travel plan before booking.",
        "user_query": state["user_query"],
        "flight_results": state["flight_results"],
        "hotel_results": state["hotel_results"],
        "itinerary": state["itinerary"],
    })

    return {
        "human_approval": decision
    }
def booking_agent(state: TravelState):

    if state["human_approval"].lower() != "yes":
        return {
            "booking_status": "cancelled",
            "booking_confirmation": "Booking cancelled by user.",
        }

    # Actual booking API will be connected here
    confirmation = "Booking request approved. Booking API integration pending."

    return {
        "booking_status": "approved",
        "booking_confirmation": confirmation,
        "messages": [
            AIMessage(content=confirmation)
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a travel itinerary.
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Final Response Agent
def final_agent(state: TravelState):

    final_prompt = f"""
    Generate final travel response.

    Flights:
    {state['flight_results']}

    Hotels:
    {state['hotel_results']}

    Itinerary:
    {state['itinerary']}
    """

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
def route_after_approval(state: TravelState):
    if state["human_approval"].lower() == "yes":
        return "booking_agent"

    return END


graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)
graph.add_node("human_approval", human_approval)
graph.add_node("booking_agent", booking_agent)
# add edge in graph 
graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", "human_approval")

graph.add_conditional_edges(
    "human_approval",
    route_after_approval,
    {
        "booking_agent": "booking_agent",
        END: END
    }
)

graph.add_edge("booking_agent", END)

# Persistent connection so both CLI and Streamlit can share the compiled app
_conn = psycopg.connect(DATABASE_URL, autocommit=True)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = graph.compile(checkpointer=checkpointer)
if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "user_aarohi"
        }
    }

    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
            "human_approval": "",
            "booking_status": "",
            "booking_confirmation": ""
        },
        config=config
    )

    # Check if workflow is waiting for human approval
    if "__interrupt__" in result:

        interrupt_data = result["__interrupt__"][0].value

        print("\n" + "=" * 60)
        print("🧑 HUMAN APPROVAL REQUIRED")
        print("=" * 60)

        print("\nUser Query:")
        print(interrupt_data["user_query"])

        print("\nFlight Results:")
        print(interrupt_data["flight_results"])

        print("\nHotel Results:")
        print(interrupt_data["hotel_results"])

        print("\nItinerary:")
        print(interrupt_data["itinerary"])

        print("\n" + "=" * 60)

        approval = input(
            "\nApprove this travel plan? (yes/no): "
        ).strip().lower()

        # Resume the interrupted graph
        result = app.invoke(
            Command(resume=approval),
            config=config
        )

    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:
        print(msg.content)
