import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

from runnables.chains.chatbot import chat

app = FastAPI(
    title="YaraAI",
    description="A conversational AI for all your needs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

chatbot = chat()

add_routes(
    app,
    chatbot,
    path="/chatbot",
)


if __name__ == "__main__":

    uvicorn.run(app, host="localhost", port=8000)
