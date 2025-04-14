# DBOS Hackathon

Welcome to the DBOS Hackathon!

Your goal is to build an application that can index financial documents into an AI model and accurately answer questions about them.
But there's a catch!
Your app has been infected by a chaos monkey that will randomly terminate it every few seconds. 🐒🐒🐒
You must use DBOS to make your app recover from failures, so it can make progress despite the chaos monkey's best efforts.

### Requirements

- You must have Python >=3.10 installed. Check your Python version with `python3 --version`.
- You must have Docker installed on your computer. Download it [here](https://docs.docker.com/engine/install/). We use Docker to run a containerized Postgres database.

### Getting Started

First, create and activate a virtual environment with:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Then, install dependencies.
In addition to DBOS, we use [LlamaIndex](https://www.llamaindex.ai/) to manage the vector index and interact with the AI model.

```shell
pip install dbos llama-index llama-index-vector-stores-postgres
```

Next, start a Postgres database and vector store using Docker:

```
dbos postgres start
```

Now, start the app:

```
python3 -m app.main
```

If everything was installed correctly, the app should prompt you:

```
Would you like to index Apple financial documents? (y/n):
```

This doesn't do anything yet--you need to implement indexing!

### The Task

Your task is to implement a pipeline that downloads, parses, and indexes documents so that the AI model can accurately answer questions about them.
Specifically, implement this stub to index Apple SEC 10-K filings for 2020-2024:

```python
def index_apple_data(index: VectorStoreIndex):
    urls = [
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2020.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2021.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2022.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2023.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2024.pdf",
    ]
    print(f"TODO: implement indexing for Apple financial documents: {urls}")
```

But be careful!
Starting the ingestion pipeline also starts a chaos monkey daemon.
After a few seconds, the chaos monkey will kill your process.
You need to add DBOS to your pipeline so it can recover from failures and make progress despite the monkey's best efforts.

After your documents are ingested, you can ask questions of the model to see if your data has been correctly ingested.
For example, you may ask it:

```
> What were Apple's earnings per share in 2020, 2021, 2022, 2023, and 2024?
```

If it's ingested all documents correctly, its answer should look something like this:

```
Thinking...

Response:
Apple's earnings per share for the years 2020 to 2024 are as follows:
- 2020: Basic EPS $3.31, Diluted EPS $3.28
- 2021: Basic EPS $5.67, Diluted EPS $5.61
- 2022: Basic EPS $6.15, Diluted EPS $6.11
- 2023: Basic EPS $6.16, Diluted EPS $6.13
- 2024: Basic EPS $6.11, Diluted EPS $6.08
```

### Resources

Here are some resources to help you get started building.

- After downloading and parsing the documents, you'll need to add them to the `VectorStoreIndex` so the AI model can answer questions about them. 
[Here](https://docs.llamaindex.ai/en/stable/module_guides/indexing/document_management/) is some documentation for adding documents to a `VectorStoreIndex`.
Each document is large (100+ pages) so you probably want to split them up instead of ingesting them all at once.
- You'll need to implement your document indexing pipeline as a DBOS workflow so it can recover from the chaos monkey. [Here](https://docs.dbos.dev/python/tutorials/workflow-tutorial) is the documenation for workflows. [Here](https://docs.dbos.dev/python/integrating-dbos) is the documentation for adding DBOS to your app.
- You can use [DBOS queues](https://docs.dbos.dev/python/tutorials/queue-tutorial) to index multiple documents concurrently.

### Scoring

Scoring is based on the total amount of time it takes for your application to ingest all documents.
To qualify, your app must:

- Be able to accurately answer questions about Apple's financial performance (such as the earnings per share question above).
- Not modify the chaos monkey in any way.

The application prints when document ingestion begins and ends--when you're done, report these print statements.
Because of the chaos monkey, ingesting documents may require restarting and recovering multiple times, so measure time starting from the very beginning of your successful ingestion, across all restarts.
The team that ingests documents the fastest is the winner!

Good luck, and may your application survive the chaos monkey's rampage!