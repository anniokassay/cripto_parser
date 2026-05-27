import requests
import time
import psycopg2
from psycopg2.extras import Json, execute_values

URL = "https://api2.bybit.com/fiat/otc/item/online"

change_type = 1 # USDT-RUB (buy USDT)

payload = {
  "tokenId": "USDT",
  "currencyId": "RUB",
  "side": "1",     # BUY
  "size": "25",
  "page": "1",
  "amount": "",
  "authMaker": False
}

headers = {
  "Content-Type": "application/json"
}

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

    rows = []  # ← ключевая строка
    
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

    with conn.cursor() as cur:
      cur.execute("INSERT INTO raw_data.load_info (load_type) VALUES (1) RETURNING id")
      load_id = cur.fetchone()[0]
      execute_values(
          cur,
          """
          INSERT INTO raw_data.data_bybit
          (change_type_id, seller, price, limit_min, limit_max, payments, load_id)
          VALUES %s
          """,
          [
              (change_type, s, p, mn, mx, pay, load_id)
              for s, p, mn, mx, pay in rows
          ],
      )

    conn.commit()
    print("Succes_insert")
    time.sleep(90)