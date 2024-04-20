import streamlit as st
from langserve import RemoteRunnable
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage
import asyncio

import server
from runnables.chains.chatbot import generate_response, stream_response


chatbot = RemoteRunnable("http://localhost:8000/chatbot/")

st.title("YaraAI")

for message in st.session_state:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

user_query = st.chat_input("Type your message here...")
if user_query:

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = stream_response(chatbot, user_query)
        st.write_stream(response)
