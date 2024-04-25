import streamlit as st
from langserve import RemoteRunnable
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage
import asyncio

import server
from runnables.utils.conversation import conversation


chatbot = RemoteRunnable("http://localhost:8000/chatbot/")

st.title("YaraAI")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("You", key="prompt")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = conversation(chatbot, prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
