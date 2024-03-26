from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder


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

summary_prompt_template = PromptTemplate.from_template(
    """Write a concise summary of the following:
                "{text}"
                Be as brief as possible, but include all the key points.
                CONCISE SUMMARY:"""
)

retrieval_qa_template = """Use the following pieces of context to answer the user's question. 
Keep the answers very brief and if you don't know the answer, 
just say that you don't know, don't try to make up an answer. Answser in French.
----------------
{context}"""
