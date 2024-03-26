import asyncio
from runnables.chains.chatbot import Chatbot

chatbot = Chatbot()


if __name__ == "__main__":

    while True:
        user_input = input("You: ")
        asyncio.run(chatbot.stream_response(user_input))
        print("\n")
    