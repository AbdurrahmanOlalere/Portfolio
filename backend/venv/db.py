import psycopg2
from psycopg2 import sql
import key as rds

def get_connection(database=None):
    return psycopg2.connect(
        host=rds.host,
        port=rds.port,
        user=rds.user,
        password=rds.password,
        database=database or rds.db,
    )

# Function to create a postgres database
def create_database(db_name):
    conn = get_connection(database='postgres')  # Connect to default db
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    conn.close()

# Table Creation
def create_Details_table():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS Details (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200),
                    email VARCHAR(200),
                    message VARCHAR(200)
                )
            """)
            cursor.execute(create_table_query)
            conn.commit()

# Function to create a table dynamically
def create_table(table_name, columns):
    with get_connection() as conn:
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

# Function to insert data into a table
def insert_into_table(table_name, data):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            columns = [col_name for col_name, _ in data]
            values = [value for _, value in data]
            insert_query = sql.SQL(
                "INSERT INTO {} ({}) VALUES ({})"
            ).format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.SQL('%s') for _ in columns)
            )
            cursor.execute(insert_query, values)
            conn.commit()

def insert_details(name, email, message):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            insert_query = sql.SQL("INSERT INTO Details (name, email, message) VALUES (%s, %s, %s)")
            cursor.execute(insert_query, (name, email, message))
            conn.commit()

# Read the data
def get_details():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Details")
            details = cursor.fetchall()
    return details


