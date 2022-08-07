import psycopg2
import os

engine = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user="postgres",
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("DB_HOST"),
    port="5432",
)

# John Cena login
get_cena = (
    "select userid from login where username = 'JohnCena' and password = 'badpass';"
)
cursor = engine.cursor()
cursor.execute(get_cena)


if engine:
    cursor.close()
    engine.close()
    print("PostgreSQL connection is closed")
