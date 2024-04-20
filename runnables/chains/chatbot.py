import asyncio

from operator import itemgetter

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, Runnable

from ..utils.llm import get_llm
from config.prompt_templates import chatbot_prompt_template

import streamlit as st


llm = get_llm()
prompt = chatbot_prompt_template
memory = ConversationBufferMemory(return_messages=True)


def chat():
    chat_chain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt
        | llm
    )
    return chat_chain


def generate_response(chatbot: Runnable, user_input: str):
    data = {"input": user_input}
    chatbot = chat()
    response = chatbot.invoke(data)
    memory.save_context(data, {"output": response})
    return response


def stream_response(chatbot: Runnable, user_input: str):
    data = {"input": user_input}
    chatbot = chat()
    response = chatbot.stream(data)
    memory.save_context(data, {"output": response})
    return response
