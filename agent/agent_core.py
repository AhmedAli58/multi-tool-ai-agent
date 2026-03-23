import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langsmith import traceable

from tools.calculator import calculator
from tools.weather import weather
from tools.news import news


def setup_langsmith():
    os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
    os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
    os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]


def build_agent():
    setup_langsmith()

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=st.secrets["GROQ_API_KEY"],
        temperature=0,
        max_tokens=2048,
    )

    tools = [calculator, weather, news]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant with access to three tools:
- calculator: use for any math or arithmetic
- weather: use for weather questions about any city
- news: use for latest news on any topic

Rules:
1. Always call the appropriate tool.
2. After getting the tool result, summarize it clearly for the user.
3. Never say you already provided a function call.
4. Be concise and friendly."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3,
        max_execution_time=30,
        handle_parsing_errors=True,
    )

    return executor


@traceable
def run_agent(executor, user_input: str, chat_history: list) -> str:
    try:
        response = executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })
        return response.get("output", "I could not generate a response.")
    except Exception as e:
        return f"Agent error: {str(e)}"