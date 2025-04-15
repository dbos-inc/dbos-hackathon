import datetime
import logging
import os

from llama_index.core import VectorStoreIndex

from .chaos_monkey import ChaosMonkey
from .index import configure_index

###########################
# Configuration
###########################


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
db_url = os.environ.get(
    "DBOS_DATABASE_URL", "postgresql://postgres:dbos@localhost:5432/dbos_hackathon"
)

# Create the vector index.
# You'll add documents to it so the model can accurately answer questions about them.
index: VectorStoreIndex
index, chat_engine = configure_index(db_url)


###########################
# Index Documents
###########################


def index_apple_data():
    urls = [
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2020.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2021.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2022.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2023.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2024.pdf",
    ]
    print(f"TODO: implement indexing for Apple financial documents: {urls}")

    # Implement your document ingestion pipeline here.
    # Download the documents, parse them, and add them to the vector index!

    # When you're done, uncomment this next line so you can measure how long document ingestion took.

    # print(f"Document ingestion completed at {datetime.datetime.now()}")


###########################
# Terminal Interface
###########################


def main():
    # Start the chaos monkey, which simulates failures by randomly terminating the process.
    ChaosMonkey.start()
    # Ask if the user wants to index documents
    index_docs = input(
        "Would you like to index Apple financial documents? (y/n): "
    ).lower()
    if index_docs == "y":
        print(f"Starting document ingestion at {datetime.datetime.now()}")
        index_apple_data()

    print("\nDocument query system ready! Type 'exit' to quit.")
    print("Ask questions about Apple financial data:\n")

    # Chat loop to ask questions of the model
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
