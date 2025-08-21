import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="AwakeGuard",   # match with your pgAdmin DB name
        user="postgres",
        password="avadhut",
        host="localhost",
        port="5432"
    )
