import psycopg2

# connect to database
engine = psycopg2.connect(
    database="depression-solved",
    password="goodpass",
    host="depression-solved.cro2y7qspvtf.us-east-2.rds.amazonaws.com",
    port="5432",
)

print(engine)
