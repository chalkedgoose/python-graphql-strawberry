import psycopg2
import os

# connect to database
engine = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user="postgres",
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("DB_HOST"),
    port="5432",
)

print(engine)
