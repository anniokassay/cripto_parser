# Код деактивирован (binance убрал fiat RUB, не отдает данные по web):
exit("Script deactivated")

import requests
import time
import psycopg2
from psycopg2.extras import Json, execute_values
import json

URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

change_type = 3 # USDT-VND (SELL USDT)

payload = {
  "asset": "USDT",
  "fiat": "VND",
  "merchantCheck": False,
  "page": 1,
  "payTypes": [],
  "publisherType": None,
  "rows": 25,
  "tradeType": "SELL"
}

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://p2p.binance.com",
    "referer": "https://p2p.binance.com/",
    "user-agent": "Mozilla/5.0"
}

session = requests.Session()

session.get("https://p2p.binance.com/")

response = session.post(
    URL,
    data=json.dumps(payload),
    headers=headers
)

print(response.text)

conn = psycopg2.connect(
    dbname="dwh",
    user="bybitparser",
    password="TokenPWforByBit",
    host="46.21.81.183",
    port="5432"
)

while True:

    response = requests.post(
        URL,
        data=json.dumps(payload),
        headers=headers
    )

    data = response.json()

    print(data)

    if not data.get("data"):
        print("No data returned")
        time.sleep(90)
        continue

    rows = []

    for item in data["data"]:

        adv = item["adv"]
        advertiser = item["advertiser"]

        row = (
            advertiser["nickName"],
            float(adv["price"]),
            float(adv["minSingleTransAmount"]),
            float(adv["dynamicMaxSingleTransAmount"]),
            Json(adv.get("tradeMethods", []))
        )

        rows.append(row)

    print(rows)

    with conn.cursor() as cur:

        cur.execute(
            "INSERT INTO raw_data.load_info (load_type) VALUES (2) RETURNING id"
        )

        load_id = cur.fetchone()[0]

        execute_values(
            cur,
            """
            INSERT INTO raw_data.data_binance
            (change_type_id, seller, price, limit_min, limit_max, payments, load_id)
            VALUES %s
            """,
            [
                (change_type, s, p, mn, mx, pay, load_id)
                for s, p, mn, mx, pay in rows
            ],
        )

    conn.commit()

    print("Success insert Binance")

    time.sleep(90)