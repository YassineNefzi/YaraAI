from fastapi import FastAPI, HTTPException, status

from chains.chatbot import Chatbot


chatbot = Chatbot()

app = FastAPI()


@app.post("/chatbot")
def talk(input: str):
    response = chatbot.generate_response(input)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No response found"
        )
    return {"response": response}
