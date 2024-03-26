import asyncio

from operator import itemgetter

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from langchain.chains import ConversationChain
from langchain.callbacks import StreamingStdOutCallbackHandler
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

    async def stream_response(self, user_input):
        data = {"input": user_input}

        async for chunk in self.chat_chain.astream(data):
            for word in chunk.split():  # Split the chunk into words
                print(word, end=" ", flush=True)
                await asyncio.sleep(0.1)

    def generate_response(self, user_input):
        data = {"input": user_input}

        response_data = self.chat_chain.invoke(data)
        # response = response_data.content

        self.memory.save_context(data, {"output": response_data})

        return response_data
