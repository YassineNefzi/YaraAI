from runnables.chains.summary import Summary

if __name__ == "__main__":

    summary = Summary()
    # example link : https://lilianweng.github.io/posts/2023-06-23-agent/
    url = input("Enter the link to the article you want to summarize: ")

    summary_text = summary.summarize(url)
    print(summary_text)
