import streamlit as st
import fastapi_client

st.title("YaraAI")

prompt = st.chat_input("What is up?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:

    st.chat_message("user").markdown(prompt)

    try:
        response_dict = fastapi_client.talk(prompt)
        response = response_dict.get("response")
    except Exception as e:
        response = f"Error: {str(e)}"
        st.error(response)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.extend(
        [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response},
        ]
    )
