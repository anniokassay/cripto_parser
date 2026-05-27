import requests
import time
import psycopg2
from psycopg2.extras import Json, execute_values
import json

URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

payload = {
    "asset": "USDT",
    "fiat": "RUB",
    "merchantCheck": False,
    "page": 1,
    "payTypes": [],
    "publisherType": None,
    "rows": 10,
    "tradeType": "BUY"
}

headers = {
    "content-type": "application/json"
}

response = requests.post(
    URL,
    headers=headers,
    data=json.dumps(payload)
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
        json=payload,
        headers=headers
    )

    data = response.json()

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