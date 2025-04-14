import logging
import os

from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import create_engine, make_url, text

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("dbos-hackathon")

###########################
# Configure Vector Index
###########################

db_url = os.environ.get(
    "DBOS_DATABASE_URL", "postgresql://postgres:dbos@localhost:5432/dbos_hackathon"
)


def configure_index():
    Settings.chunk_size = 512
    url = make_url(db_url)

    # Create the index database if it does not exist
    conn_string = (
        f"postgresql://{url.username}:{url.password}@{url.host}:{url.port}/postgres"
    )
    engine = create_engine(conn_string)
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        result = conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{url.database}'")
        )
        db_exists = result.scalar() is not None
        if not db_exists:
            conn.execute(text(f"CREATE DATABASE {url.database}"))
            print(f"Database '{url.database}' created successfully.")

    # Create the vector index
    vector_store = PGVectorStore.from_params(
        database=url.database,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
    )
    vector_store._initialize()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex([], storage_context=storage_context)
    chat_engine = index.as_chat_engine()
    return index, chat_engine

index, chat_engine = configure_index()

###########################
# Index Documents
###########################


def index_apple_data(index):
    urls = [
        "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/faab4555-c69b-438a-aaf7-e09305f87ca3.pdf",
        "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/b4266e40-1de6-4a34-9dfb-8632b8bd57e0.pdf",
        "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/42ede86f-6518-450f-bc88-60211bf39c6d.pdf",
    ]
    print(f"Indexing Apple Financial Documents: {urls}")
    # TODO: Implement document indexing


###########################
# Terminal Interface
###########################


def main():
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
