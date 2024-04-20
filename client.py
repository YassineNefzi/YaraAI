import streamlit as st
from langserve import RemoteRunnable

import server
from runnables.chains.chatbot import generate_response


yara = RemoteRunnable("http://localhost:8000/chatbot/")

st.title("YaraAI")

prompt = st.chat_input("What is up?")

if prompt:
    response = generate_response(yara, prompt)
    st.write(response)
