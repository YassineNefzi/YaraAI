import streamlit as st
import fastapi_client  # Replace with your actual client code

st.title("YaraAI")

prompt = st.chat_input("What is up?")

# Initialize chat history (modify as needed based on backend calls)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Call FastAPI backend for response
    try:
        response_dict = fastapi_client.talk(prompt)
        response = response_dict.get("response")
    except Exception as e:
        response = f"Error: {str(e)}"
        st.error(response)

    # Display response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Update chat history (adjust based on backend calls)
    st.session_state.messages.extend([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ])
