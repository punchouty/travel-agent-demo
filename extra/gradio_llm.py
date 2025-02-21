import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from typing import TypedDict, Dict
from langchain_openai.chat_models import ChatOpenAI

# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL = "gpt-4o-mini"
openai = OpenAI();


system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        ##response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content


######################
from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0);


class State(TypedDict):
    query:str
    category:str
    sentiment:str
    response:str


## functions

def intent_indentification(state: State) -> State:
    """Categorize the query."""
    prompt = ChatPromptTemplate.from_template(
        "You are a flight ai assistant. Categorize the following customer query into one of these categories: "
        "get user booking details, do flight booking, cancel existing flight booking or any other. Query: {query}"
    )
    chain = prompt | llm
    category = chain.invoke({"query": state["query"]}).content
    return {"category": category}

def sentiment_analysis(state: State) -> State:
    """Analyze sentiment of the query."""
    prompt = ChatPromptTemplate.from_template(
        "Analyze the sentiment of the following customer query "
        "Response with either 'Positive', 'Neutral', or 'Negative'. Query: {query}"
    )
    chain = prompt | llm
    sentiment = chain.invoke({"query": state["query"]}).content
    return {"sentiment": sentiment}

def get_booking(state: State) -> State:
    """Do the booking"""
    return {"response": "done"}

def do_booking(state: State) -> State:
    """Do the booking"""
    return {"response": "done"}

def escalate(state: State) -> State:
    """Do the booking"""
    return {"response": "done"}

def handle_general(state: State)->State:
  prompt = ChatPromptTemplate.from_template(
      "Provide a general support response to the following query : {query}"
  )
  chain = prompt | llm
  response = chain.invoke({"query": state["query"]}).content
  return {"response": response}

def route_query(state: State)->State:
  if state["sentiment"] == "Negative":
    return "escalate"
  elif state["category"] == "get_booking":
    return "get_booking"
  elif state["category"] == "do_booking":
    return "do_booking"
  else:
    return "handle_general"
## Create and configure the graph

workflow=StateGraph(State)

workflow.add_node("intent_indentification", intent_indentification);
workflow.add_node("sentiment_analysis", sentiment_analysis);
workflow.add_node("get_booking",get_booking);
workflow.add_node("do_booking",do_booking);
workflow.add_node("escalate",escalate);
workflow.add_node("handle_general",handle_general);

workflow.add_edge("intent_indentification","sentiment_analysis");
workflow.add_conditional_edges("sentiment_analysis",
                               route_query,
                               {"get_booking":"get_booking",
                                           "do_booking":"do_booking",
                                            "escalate":"escalate",
                                            "handle_general":"handle_general"})

workflow.add_edge("get_booking", END)
workflow.add_edge("do_booking", END)
workflow.add_edge("escalate", END)
workflow.add_edge("handle_general", END)

workflow.set_entry_point("intent_indentification")

app  = workflow.compile()

def run_customer_support(query: str)->Dict[str, str]:
  results = app.invoke({"query": query})
  return {
      "category":results['category'],
      "sentiment":results['sentiment'],
      "response": results['response']
  }


def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    results = app.invoke({"query": message})

    response = openai.chat.completions.create(model=MODEL, messages=messages)
    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        ##response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content





######################

gr.ChatInterface(fn=chat, type="messages").launch()