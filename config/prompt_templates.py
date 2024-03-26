from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


chatbot_prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI assistant called Yara.",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
)