import os

from .index import configure_index

db_url = os.environ.get(
    "DBOS_DATABASE_URL", "postgresql://postgres:dbos@localhost:5432/dbos_hackathon"
)

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
