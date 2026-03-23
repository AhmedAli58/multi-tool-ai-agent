import streamlit as st
from agent.agent_core import build_agent, run_agent
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(
    page_title="Multi-Tool AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Multi-Tool AI Agent")
st.caption("Powered by LangChain + Groq | Tools: Calculator, Weather, News")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "executor" not in st.session_state:
    with st.spinner("Initializing agent..."):
        st.session_state.executor = build_agent()

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

user_input = st.chat_input("Ask me anything — math, weather, or news...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = run_agent(
                st.session_state.executor,
                user_input,
                st.session_state.chat_history
            )
        st.markdown(response)

    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response))