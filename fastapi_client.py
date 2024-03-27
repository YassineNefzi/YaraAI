from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio


from runnables.chains.chatbot import Chatbot


chatbot = Chatbot()

app = FastAPI()


@app.post("/chat")
def generate_response(input: str):
    response = chatbot.generate_response(input)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No response found"
        )
    return {"response": response}


@app.post("/chat/stream")
async def stream_response(input: str):
    pass


@app.post("/summarize")
def summarize_text(text: str):
    pass


@app.post("/extract")
def retrieve_qa(text: str):
    pass
