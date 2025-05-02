# DBOS Hackathon

Welcome to the DBOS Hackathon!

Your goal is to build an application that can index financial documents into a vector store so an AI model can accurately answer questions about them.
But there's a catch!
Inside your application lives a chaos monkey that will randomly terminate it every few seconds. 🐒🐒🐒
You must use DBOS to make your app recover from failures, so it can make progress despite the chaos monkey's best efforts.

## Requirements

- You must have Python >=3.10 installed. Check your Python version with `python3 --version`.
- You must have Docker installed on your computer. Download it [here](https://docs.docker.com/engine/install/). The app uses Docker to run a containerized Postgres database.
- You need an OpenAI API key. It must be available as an environment variable: `export OPENAI_API_KEY=...`.

## Getting Started

First, clone this repository to a local folder and enter the folder.
```shell
git clone https://github.com/dbos-inc/dbos-hackathon.git
cd dbos-hackathon
```

Then, create and activate a virtual environment in your folder with:

**macOS/Linux**
```shell
python3 -m venv .venv
source .venv/bin/activate
```


<details><summary><strong>Windows PowerShell</strong></summary>

```
python3 -m venv .venv
.venv\Scripts\activate.ps1
```
</details>


<details><summary><strong>Windows cmd</strong></summary>
    
```
python3 -m venv .venv
.venv\Scripts\activate.bat
```    
</details>


Then, install dependencies.
In addition to DBOS, the app uses [LlamaIndex](https://www.llamaindex.ai/) to manage the vector index and interact with the AI model.

```shell
pip install -r requirements.txt --upgrade
```

Next, start a Postgres database using Docker. We'll use it as a vector store.

```
docker pull pgvector/pgvector:pg16
dbos postgres start
```

Then, set the OpenAI API key as an enviroment variable:

**macOS/Linux**
```
export OPENAI_API_KEY=<your-key>
```

<details><summary><strong>Windows PowerShell</strong></summary>

```
$env:OPENAI_API_KEY = <your-key>
```
</details>


<details><summary><strong>Windows cmd</strong></summary>
    
```
set OPENAI_API_KEY=<your-key>
```    
</details>

Now, start the app:

```
python -m app.main
```

If everything was installed correctly, the app should prompt you:

```
Would you like to index Apple financial documents from the beginning? (y/n):
```

This will start indexing documents &mdash; but before it completes, the chaos monkey will kill it!

## The Task

Your task is to implement a durable pipeline that downloads, parses, and indexes documents so that the AI model can accurately answer questions about them. We already implemented some basic functions to index Apple SEC 10-K filings for 2020-2024:

```python
###########################
# Index Documents
# TODO: Make this a durable pipeline that can handle failures, and optimize its performance.
###########################

def index_document(url: str) -> int:
    ...

def index_apple_data():
    urls = [
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2020.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2021.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2022.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2023.pdf",
        "https://dbos-hackathon.s3.us-east-1.amazonaws.com/apple-filings/apple-10k-2024.pdf",
    ]
    indexed_pages = 0
    for url in urls:
        num_pages = index_document(url)
        indexed_pages += num_pages

    # Measure how long document ingestion took.
    print(f"Document ingestion completed at {datetime.datetime.now()}. Indexed {indexed_pages} pages.")
```

But be careful!
A chaos monkey daemon is also running in your application!
After a few seconds, the chaos monkey will kill your process.
You need to turn your document ingestion pipeline into a DBOS durable workflow so it can recover from failures and make progress despite the monkey's best efforts.

If you correctly add DBOS to your code, when you restart your app after crashes, your app should print something like:
```
15:36:34 [    INFO] (dbos:_dbos.py:485) Recovering <N> workflows from application version ...
```

Congrats! You no longer need to restart document ingestion from the beginning after crashes.
DBOS will automatically recover your document ingestion workflow from where it left off.

After your documents are ingested, you can ask questions of the model to see if your data has been correctly ingested.
For example, you can ask it:

```
> What was Apple's basic earnings per share and diluted EPS in 2020?
```

If it's ingested all documents correctly, its answer should look something like this:

```
Thinking...

Response:
Apple's basic earnings per share in 2020 was $3.31, and the diluted earnings per share was $3.28.
```

You can ask other questions about Apple's financial performance for different years (between 2020 to 2024) and get reasonable answers:

```
> What was Apple's basic earnings per share and diluted EPS in 2021?

Thinking...

Response:
Apple's basic earnings per share in 2021 was $5.67, and the diluted earnings per share was $5.61.
```

```
> What was Apple's basic earnings per share and diluted EPS in 2022?

Thinking...

Response:
Apple's basic earnings per share in 2022 was $5.67, and the diluted earnings per share in 2022 would be $5.61.
```

```
> What was Apple's basic earnings per share and diluted EPS in 2023?

Thinking...

Response:
Apple's basic earnings per share in 2023 was $6.16, and the diluted earnings per share was $6.13.
```

```
> What was Apple's basic earnings per share and diluted EPS in 2024?

Thinking...

Response:
Apple's basic earnings per share in 2024 was $6.11, and the diluted earnings per share was $6.08.
```

## Resources & Tips

Here are some resources and tips to help you get started building.

- You'll need to implement your document indexing pipeline as a DBOS workflow so it can recover from the chaos monkey. [Here](https://docs.dbos.dev/python/tutorials/workflow-tutorial) is the documenation for workflows. [Here](https://docs.dbos.dev/python/integrating-dbos) is the documentation for adding DBOS to your app.
- You can use [DBOS queues](https://docs.dbos.dev/python/tutorials/queue-tutorial) to index multiple documents concurrently.
- To reset your database between runs (including both your vector store and DBOS workflow metadata) run `python reset.py`.
- This app uses a LlamaIndex `VectorStoreIndex` to index documents so the AI model can answer questions about them. Learn more about it [here](https://docs.llamaindex.ai/en/stable/module_guides/indexing/document_management/).

## Scoring

Scoring is based on the total amount of time it takes for your application to ingest all documents.
To qualify, your app must:

- Be able to accurately answer questions about Apple's financial performance (such as the earnings per share questions above).
- Not modify the chaos monkey in any way.

The application prints when document ingestion begins and ends--when you're done, report those times.
```
Starting document ingestion at [start time]
...

Document ingestion completed at [end time]. Indexed 468 pages.
```
Because of the chaos monkey, ingesting documents may require restarting and recovering multiple times, so measure time starting from the very beginning of your successful ingestion, across all restarts.
The team that ingests documents the fastest is the winner!

Good luck, and may your application survive the chaos monkey's rampage!
