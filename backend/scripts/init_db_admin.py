import os
import psycopg2
from psycopg2 import sql

def get_conn_from_env():
    return psycopg2.connect(
        host=os.environ.get("PGHOST","localhost"),
        port=os.environ.get("PGPORT","5433"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        database=os.environ.get("PGDATABASE","portfoliodb"),
    )

def init():
    q = sql.SQL("""
    CREATE TABLE IF NOT EXISTS public.Details (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200),
        email VARCHAR(200),
        message VARCHAR(200)
    );
    """)
    with get_conn_from_env() as conn:
        with conn.cursor() as cur:
            cur.execute(q)
        conn.commit()
    print("Done: Details table created/ensured.")

if __name__ == "__main__":
    init()