import streamlit as st
from langserve import RemoteRunnable
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage
import asyncio

import server
from runnables.chains.chatbot import generate_response

chatbot = RemoteRunnable("http://localhost:8000/chatbot/")

st.title("YaraAI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = generate_response(chatbot, prompt)
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
