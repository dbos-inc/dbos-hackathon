from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.openai import (OpenAIEmbedding,
                                           OpenAIEmbeddingModelType)
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import create_engine, make_url, text


def configure_index(db_url: str):
    Settings.chunk_size = 512
    Settings.embed_model = OpenAIEmbedding(
        model=OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE
    )
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
        embed_dim=3072,
    )
    vector_store._initialize()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex([], storage_context=storage_context)
    chat_engine = index.as_chat_engine()
    return index, chat_engine
