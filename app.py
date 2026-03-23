import streamlit as st
import time
from agent.agent_core import build_agent, run_agent
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(
    page_title="Multi-Tool AI Agent",
    page_icon="🤖",
    layout="centered"
)

with st.sidebar:
    st.title("🤖 AI Agent")
    st.markdown("---")
    st.markdown("### 🛠️ Available Tools")
    st.success("🧮 Calculator")
    st.success("🌤️ Weather")
    st.success("📰 News")
    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    st.info("What is 25 * 48?")
    st.info("Weather in Tokyo")
    st.info("Latest news on AI")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    st.markdown("---")
    st.caption("Powered by LangChain + Groq + LangSmith")

st.title("🤖 Multi-Tool AI Agent")
st.caption("Ask me anything — I can calculate, check weather, and fetch news.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "executor" not in st.session_state:
    with st.spinner("Initializing agent..."):
        st.session_state.executor = build_agent()

if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        st.markdown("Hi! I'm your AI agent. I can help you with:\n\n- 🧮 **Math calculations**\n- 🌤️ **Weather updates**\n- 📰 **Latest news**\n\nWhat would you like to know?")

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
            start = time.time()
            response = run_agent(
                st.session_state.executor,
                user_input,
                st.session_state.chat_history
            )
            elapsed = round(time.time() - start, 2)
        st.markdown(response)
        st.caption(f"⏱️ Response time: {elapsed}s")

    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response))