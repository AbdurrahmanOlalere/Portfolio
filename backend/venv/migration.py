import psycopg2
from psycopg2 import sql
import key as rds   # This should contain your OWNER user credentials

def get_owner_connection(database=None):
    return psycopg2.connect(
        host=rds.host,
        port=rds.port,
        user=rds.owner_user,        
        password=rds.owner_password,
        database=database or rds.db
    )

# Create a database if it doesn't exist (optional)
def create_database(db_name):
    conn = get_owner_connection(database="postgres")
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created.")
        else:
            print(f"Database '{db_name}' already exists.")
    conn.close()

# Create the Details table
def create_details_table():
    with get_owner_connection() as conn:
        with conn.cursor() as cursor:
            create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS public.details (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200),
                    email VARCHAR(200),
                    message TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
                )
            """)
            cursor.execute(create_table_query)
            
            # Grant permissions to the RW app user
            cursor.execute(sql.SQL("GRANT INSERT, SELECT, UPDATE, DELETE ON public.details TO {}").format(
                sql.Identifier(rds.user)  # ← svc_portfolio_rw
            ))
            cursor.execute(sql.SQL("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {}").format(
                sql.Identifier(rds.user)
            ))
            
            conn.commit()
            print("Table created and permissions granted to", rds.user)

# Generic table creation function
def create_table(table_name, columns):
    with get_owner_connection() as conn:
        with conn.cursor() as cursor:
            create_table_query = sql.SQL(
                "CREATE TABLE IF NOT EXISTS {} ({})"
            ).format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(
                    sql.SQL("{} {}").format(
                        sql.Identifier(col_name),
                        sql.SQL(col_type)
                    ) for col_name, col_type in columns
                )
            )
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Table '{table_name}' ensured.")

if __name__ == "__main__":
    print("Running migrations...") 
    create_details_table() 
    print("Migrations complete.")