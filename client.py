import streamlit as st
from langserve import RemoteRunnable

import server


llm = RemoteRunnable("http://localhost:8000/chatbot/")

st.title("YaraAI")

prompt = st.chat_input("What is up?")

if prompt:
    response = llm.invoke(prompt)
    st.write(response)
