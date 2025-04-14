import os

from llama_index.core import VectorStoreIndex

from .index import configure_index

db_url = os.environ.get(
    "DBOS_DATABASE_URL", "postgresql://postgres:dbos@localhost:5432/dbos_hackathon"
)

###########################
# Index Documents
###########################


def index_apple_data(index: VectorStoreIndex):
    urls = [
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2020.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2021.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2022.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2023.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2024.pdf",
    ]
    print(f"Indexing Apple Financial Documents: {urls}")
    # TODO: Implement document indexing


###########################
# Terminal Interface
###########################


def main():
    print("Initializing document query system...")
    index, chat_engine = configure_index(db_url)
    # Ask if user wants to index documents
    index_docs = input(
        "Would you like to index Apple financial documents? (y/n): "
    ).lower()
    if index_docs == "y":
        index_apple_data(index)

    print("\nDocument query system ready! Type 'exit' to quit.")
    print("Ask questions about Apple financial data:\n")

    # Main interaction loop
    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break

        print("Thinking...")
        response = str(chat_engine.chat(user_input))
        print("\nResponse:")
        print(response)
        print()


if __name__ == "__main__":
    main()
