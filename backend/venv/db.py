import psycopg2
from psycopg2 import sql
import key as rds

# Connection setup
conn = psycopg2.connect(
    host=rds.host,
    port=rds.port,
    user=rds.user,
    password=rds.password,
    database=rds.db,
)


#Table Creation
#cursor = conn.cursor()
#create_table="""
#create table Details (id INT NOT NULL AUTO_INCREMENT,name varchar(200),email varchar(200),message varchar(200),PRIMARY KEY (id))
#"""
#cursor.execute(create_table)

# Table Creation
def create_Details_table():
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

# Function to create a table
def create_table(table_name, columns):
    with conn.cursor() as cursor:
        # Generate the CREATE TABLE query dynamically , i'mtrying to make this a bit more flexible, maybe i should make a funciton with more args like not primary keys and such
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
    with conn.cursor() as cursor:
        # Generate the INSERT INTO query dynamically
        insert_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({})"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(sql.Identifier(col_name) for col_name, _ in data),
            sql.SQL(', ').join(sql.Placeholder() for _, value in data)
        )
        cursor.execute(insert_query, [value for _, value in data])
        conn.commit()


def insert_details(name,email,message):
    with conn.cursor() as cursor:
        insert_query = sql.SQL("INSERT INTO Details (name, email, message) VALUES (%s, %s, %s)")
        cursor.execute(insert_query, (name, email, message))
        conn.commit()

# Read the data
def get_details():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Details")
        details = cursor.fetchall()
    return details

#create_Details_table() use this to create an inital table