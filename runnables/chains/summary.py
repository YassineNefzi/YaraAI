from langchain.chains.summarize import load_summarize_chain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from ..utils.llm import get_llm
from config.prompt_templates import summary_prompt_template

llm = get_llm()

summary_chain = LLMChain(
    llm=llm,
    prompt=summary_prompt_template,
)

stuff_chain = StuffDocumentsChain(
    llm_chain=summary_chain, document_variable_name="text"
)
