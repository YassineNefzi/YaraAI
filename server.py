from fastapi import FastAPI
import uvicorn
from langserve import add_routes
from langchain_google_genai import ChatGoogleGenerativeAI

from runnables.utils.llm import _get_llm

llm = _get_llm()

app = FastAPI(
    title="YaraAI",
    description="A conversational AI for all your needs",
)

add_routes(
    app,
    llm,
    path="/chatbot",
)


if __name__ == "__main__":

    uvicorn.run(app, host="localhost", port=8000)
