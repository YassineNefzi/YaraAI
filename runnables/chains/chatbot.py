import asyncio
import time

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


def chat_chain():
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
    response = chatbot.invoke(data)
    memory.save_context(data, {"output": response})
    return response


async def stream_response(chatbot: Runnable, user_input: str):
    data = {"input": user_input}
    response_chunks = []
    async for chunk in chatbot.astream(data):
        response_chunks.append(chunk)
        for char in chunk:
            print(char, end="", flush=True)
            # yield char
            await asyncio.sleep(0.01)
        memory.save_context(data, {"output": "".join(response_chunks)})
