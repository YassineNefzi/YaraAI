import asyncio

from langchain.chains.summarize import load_summarize_chain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.document_loaders.web_base import WebBaseLoader

from ..utils.llm import get_llm
from config.prompt_templates import summary_prompt_template


class Summary:
    def __init__(self):
        self.llm = get_llm()
        self.summary_chain = LLMChain(
            llm=self.llm,
            prompt=summary_prompt_template,
        )

        self.stuff_chain = StuffDocumentsChain(
            llm_chain=self.summary_chain, document_variable_name="text"
        )

    def link_summarize(self, text):
        loader = WebBaseLoader(text)
        docs = loader.load()

        summary = self.stuff_chain.invoke(docs)

        return summary.get("output_text")
