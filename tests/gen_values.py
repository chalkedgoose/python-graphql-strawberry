from socket import send_fds
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
uuid = cursor.fetchone()[0]

import requests
import json


def test_sad(text: str = "") -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {os.environ["OPENAPI_KEY"]}',
    }
    print(text)
    data = (
        r'{"model": "text-davinci-002", "prompt": "Sentence: '
        + text.replace('"', "")
        + r'        Suicidality from 0 - 100:", "temperature": 0, "max_tokens": 220}'
    )
    r = requests.post(
        "https://api.openai.com/v1/completions", headers=headers, data=data
    )
    pretty = json.loads(r.text)
    return pretty["choices"][0]["text"].strip().split()[0]


import random

try:
    if input("tweets?") != "q":
        while 1:
            tweet = input("tweet: ").encode("ascii", "ignore").decode()

            rating = test_sad(tweet)
            tweet = tweet.replace("'", "''")
            special = "', '".join([f"{random.randint(0, 1000)}" for i in range(6)])
            send_cena = (
                f"insert into PHATtable(UUID, date, IMGfilepath, MECHID1, MECHID2, "
                f"MECHID3, VALUESID1, VALUESID2, VALUESID3, memoText, MemoGPTrating) "
                f"VALUES('{uuid}', '{1659866339 + random.randint(-10000000, 10000000)}', "
                f"'/random/user', '{special}', '{tweet}', '{rating}')"
            )
            cursor.execute(send_cena)
            engine.commit()
except Exception as e:
    print(e)
finally:
    if engine:
        cursor.close()
        engine.close()
        print("PostgreSQL connection is closed")
