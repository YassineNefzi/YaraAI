from langchain_community.document_loaders.web_base import WebBaseLoader

from runnables.chains.summary import summary_chain, stuff_chain

if __name__ == "__main__":
    # example link : https://lilianweng.github.io/posts/2023-06-23-agent/
    url = input("Enter the link to the article you want to summarize: ")

    loader = WebBaseLoader(url)
    docs = loader.load()

    summary = stuff_chain.invoke(docs)
    print(summary.get("output_text"))
