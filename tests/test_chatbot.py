from runnables.chains.chatbot import Chatbot

chatbot = Chatbot()

if __name__ == "__main__":
    chatbot = Chatbot()

    while True:
        user_input = input("You: ")
        response = chatbot.generate_response(user_input)
        print(response)
