from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio


from runnables.chains.chatbot import Chatbot


chatbot = Chatbot()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def talk(input: str):
    response = chatbot.generate_response(input)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No response found"
        )
    return {"response": response}


# @app.websocket("/chat")
# async def websocket_talk(ws: WebSocket):
#     await ws.accept()
#     while True:
#         prompt = await ws.receive_text()
#         response = chatbot.stream_response(prompt)
#         await ws.send_text(response)


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive()
            if data is None:
                break

            async for word in chatbot.stream_response(data):
                await websocket.send(word)
                await asyncio.sleep(0.1)  # Adjust delay for streaming effect

    except WebSocketDisconnect:
        pass
