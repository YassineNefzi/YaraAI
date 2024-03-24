import getpass
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory

load_dotenv()

api_key = os.environ.get('GOOGLE_API_KEY')

class Chatbot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model='gemini-pro', 
                                          google_api_key=api_key,
                                          convert_system_message_to_human=True )
        self.memory = ConversationBufferMemory(return_messages=True)
        self.prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "You are an AI assistant called Yara.",
                        ),
                        MessagesPlaceholder("history"),
                        ("human", "{input}"),
                    ]
                )
        self.chat_chain = ConversationChain(
            llm=self.llm, prompt=self.prompt, memory=self.memory, verbose=True
        )

    def generate_response(self, user_input):
        data = {"input": user_input}
        response_data = self.chat_chain.invoke(data)  # Invoke the chat chain
        # Extract only the response from the returned data
        response = response_data.get("response")
        return response