import os
from dotenv import load_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from config.prompt_templates import retrieval_qa_template
from ..utils.llm import get_llm

load_dotenv()

pdf_path = os.environ.get("PDF_PATH")

messages = [
    SystemMessagePromptTemplate.from_template(retrieval_qa_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]

CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def retrieve_from_pdf(query: str):
    """Retrieves information from a PDF document based on a given query."""

    llm = get_llm()
    loader = DirectoryLoader(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    documents = loader.load()
    texts = text_splitter.split_documents(documents)
    db = Chroma.from_documents(embedding=HuggingFaceEmbeddings(), documents=texts)
    retriever = db.as_retriever()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | CHAT_PROMPT
        | llm
    )
    answer = rag_chain.invoke(query)
    return answer
