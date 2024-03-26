from runnables.chains.retrieval_qa import retrieve_from_pdf

if __name__ == "__main__":
    query = input("Enter your question: ")
    answer = retrieve_from_pdf(query)
    print(answer)
