import os
import psycopg2
from psycopg2 import sql

def main():
    conn = psycopg2.connect(
        host=os.environ.get("PGHOST","localhost"),
        port=os.environ.get("PGPORT","5433"),
        user=os.environ.get("PGUSER","postgres"),
        password=os.environ.get("PGPASSWORD"),
        database=os.environ.get("PGDATABASE","portfoliodb"),
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS public.details (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200),
                email VARCHAR(200),
                message TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            );
            """)
            cur.execute("GRANT INSERT, SELECT, UPDATE, DELETE ON public.details TO myportfolioserviceuser;")
            cur.execute("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO myportfolioserviceuser;")
    print("Done: details table ensured and privileges granted.")

if __name__ == '__main__':
    main()