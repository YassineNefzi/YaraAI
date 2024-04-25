import streamlit as st
from langserve import RemoteRunnable
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage
import asyncio

import server
from runnables.utils.conversation import conversation


chatbot = RemoteRunnable("http://localhost:8000/chatbot/")

st.title("YaraAI")

prompt = st.chat_input("What is up?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        conversation(chatbot, prompt)

    # st.session_state.messages.extend([
    #     {"role": "user", "content": prompt},
    #     {"role": "assistant", "content":}
    # ])
