import asyncio

from operator import itemgetter

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from ..utils.llm import get_llm
from config.prompt_templates import chatbot_prompt_template


class Chatbot:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = chatbot_prompt_template
        self.memory = ConversationBufferMemory(return_messages=True)
        self.chat_chain = (
            RunnablePassthrough.assign(
                history=RunnableLambda(self.memory.load_memory_variables)
                | itemgetter("history")
            )
            | self.prompt
            | self.llm
        )
