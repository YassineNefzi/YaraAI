import getpass
import os
from dotenv import load_dotenv
import asyncio

from operator import itemgetter

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")


class Chatbot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            convert_system_message_to_human=True,
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI assistant called Yara.",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        self.memory = ConversationBufferMemory(return_messages=True)
        self.parser = StrOutputParser()
        self.chat_chain = (
            RunnablePassthrough.assign(
                history=RunnableLambda(self.memory.load_memory_variables)
                | itemgetter("history")
            )
            | self.prompt
            | self.llm
            | self.parser
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

if __name__ == "__main__":
    chatbot = Chatbot()

    while True:
        user_input = input("You: ")
        asyncio.run(chatbot.stream_response(user_input))
        print("\n")
    
    
    