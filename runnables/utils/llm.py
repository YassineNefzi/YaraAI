import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

google_api_key = os.environ.get("GOOGLE_API_KEY")

def _get_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=google_api_key,
        temperature=0,
        convert_system_message_to_human=True,
        max_retries=2,
    )

def get_llm():
    return _get_llm() | StrOutputParser()