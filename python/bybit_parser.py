import requests
import time
import psycopg2
import os
from psycopg2.extras import Json, execute_values

URL = "https://api2.bybit.com/fiat/otc/item/online"

headers = {
    "Content-Type": "application/json"
}

# Конфигурация пар
markets = [
    {
        "change_type": 1,
        "payload": {
            "tokenId": "USDT",
            "currencyId": "RUB",
            "side": "1",  # BUY USDT
            "size": "25",
            "page": "1",
            "amount": "",
            "authMaker": False
        }
    },
    {
        "change_type": 3,
        "payload": {
            "tokenId": "USDT",
            "currencyId": "VND",
            "side": "0",  # SELL USDT
            "size": "25",
            "page": "1",
            "amount": "",
            "authMaker": False
        }
    }
]

def required_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


conn = psycopg2.connect(
    dbname=required_env("DB_NAME"),
    user=required_env("DB_USER"),
    password=required_env("DB_PASSWORD"),
    host=required_env("DB_HOST"),
    port=required_env("DB_PORT")
)

while True:

    for market in markets:

        change_type = market["change_type"]
        payload = market["payload"]

        response = requests.post(
            URL,
            json=payload,
            headers=headers
        )

        data = response.json()

        if not data.get("result"):
            print(f"No result for change_type={change_type}")
            continue

        rows = []

        for item in data["result"]["items"]:

            row = (
                item["nickName"],
                float(item["price"]),
                float(item["minAmount"]),
                float(item["maxAmount"]),
                Json([
                    p["paymentType"] if isinstance(p, dict) else p
                    for p in item.get("payments", [])
                ])
            )

            rows.append(row)

        if not rows:
            print(f"No rows for change_type={change_type}")
            continue

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO raw_data.load_info (load_type)
                VALUES (1)
                RETURNING id
                """
            )

            load_id = cur.fetchone()[0]

            execute_values(
                cur,
                """
                INSERT INTO raw_data.data_bybit
                (
                    change_type_id,
                    seller,
                    price,
                    limit_min,
                    limit_max,
                    payments,
                    load_id
                )
                VALUES %s
                """,
                [
                    (change_type, s, p, mn, mx, pay, load_id)
                    for s, p, mn, mx, pay in rows
                ],
            )

        conn.commit()

        print(f"Success insert change_type={change_type}")

    time.sleep(90)