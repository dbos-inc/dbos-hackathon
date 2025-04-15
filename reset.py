# Reset your application, both the vector store and DBOS system database.

import os

from sqlalchemy import create_engine, make_url, text

db_url = os.environ.get(
    "DBOS_DATABASE_URL", "postgresql://postgres:dbos@localhost:5432/dbos_hackathon"
)


def reset():
    print(f"Resetting DBOS Hackathon database")
    url = make_url(db_url)
    conn_string = (
        f"postgresql://{url.username}:{url.password}@{url.host}:{url.port}/postgres"
    )
    engine = create_engine(conn_string)
    vector_store, sys_db = url.database, f"{url.database}_dbos_sys"
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        for db in [vector_store, sys_db]:
            conn.execute(text(f"DROP DATABASE IF EXISTS {db} WITH (FORCE)"))
    print(f"DBOS Hackathon database successfully reset")


if __name__ == "__main__":
    reset()
