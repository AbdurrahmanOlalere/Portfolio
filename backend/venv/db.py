import pymysql
import key as rds
conn = pymysql.connect(
	    host = rds.host,
        port = int(rds.port),
        user = rds.user,
	    password = rds.password,
        db = rds.db,
    )

#Table Creation
#cursor = conn.cursor()
#create_table="""
#create table Details (id INT NOT NULL AUTO_INCREMENT,name varchar(200),email varchar(200),message varchar(200),PRIMARY KEY (id))
#"""
#cursor.execute(create_table)

def insert_details(name,email,message):
    cur=conn.cursor()
    cur.execute("INSERT INTO Details (name,email,message) VALUES(%s,%s,%s)",(name,email,message))
    conn.commit()
    
#read the data
def get_details():
    cur=conn.cursor()
    cur.execute("SELECT * FROM portfoliodb.Details") # find out how to create placeholder for this
    details = cur.fetchall()
    return details