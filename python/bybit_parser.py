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


def log_error(conn, load_type, error_description):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO raw_data.load_info (load_type)
            VALUES (%s)
            RETURNING id
            """,
            (load_type,)
        )
        load_id = cur.fetchone()[0]
        cur.execute(
            """
            INSERT INTO raw_data.load_error_log (load_id, error_description)
            VALUES (%s, %s)
            """,
            (load_id, error_description)
        )


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

        try:
            response = requests.post(
                URL,
                json=payload,
                headers=headers,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            result = data.get("result")
            if not result:
                error_text = f"API ERROR change_type={change_type}: empty result"
                log_error(conn, 1, error_text)
                conn.commit()
                print(error_text)
                continue

            items = result.get("items", [])
            if not items:
                print(f"No items for change_type={change_type}")
                continue

            rows = []

            for item in items:
                try:
                    seller = item.get("nickName", "unknown")
                    price = float(item.get("price", 0))
                    min_limit = float(item.get("minAmount", 0))
                    max_limit = float(item.get("maxAmount", 0))
                    payments = [
                        p.get("paymentType") if isinstance(p, dict) else p
                        for p in item.get("payments", [])
                    ]

                    row = (
                        seller,
                        price,
                        min_limit,
                        max_limit,
                        Json(payments)
                    )
                    rows.append(row)

                except Exception as parse_error:
                    error_text = f"PARSE ERROR change_type={change_type}: {parse_error}"
                    log_error(conn, 1, error_text)
                    conn.commit()
                    print(error_text)

            if not rows:
                print(f"No parsed rows for change_type={change_type}")
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
            print(f"Success insert change_type={change_type}, rows={len(rows)}")

        except Exception as e:
            conn.rollback()

            error_text = f"ERROR change_type={change_type}: {e}"
            try:
                log_error(conn, 1, error_text)
                conn.commit()
            except Exception as log_error_exc:
                conn.rollback()
                print(f"LOG ERROR change_type={change_type}: {log_error_exc}")

            print(error_text)

    time.sleep(90)