import streamlit as st
from langchain_core.runnables import Runnable

from runnables.chains.chatbot import chat_chain, stream_response


def conversation(chatbot: Runnable, user_input: str):

    response_chunks = []
    for chunk in stream_response(chatbot, user_input):
        response_chunks.append(chunk)

    st.write_stream(stream_response(chatbot, user_input))

    return "".join(response_chunks)
