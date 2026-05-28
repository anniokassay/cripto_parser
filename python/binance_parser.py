exit() #API ERROR change_type=5: code=000002
import requests
import time
import psycopg2
import os

from psycopg2.extras import Json, execute_values

URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

markets = [
    {
        # Продать USDT за CNY
        "change_type": 5,
        "payload": {
            "fiat": "CNY",
            "page": 1,
            "rows": 25,
            "tradeType": "SELL",
            "asset": "USDT",
            "countries": [],
            "proMerchantAds": False,
            "shieldMerchantAds": False,
            "publisherType": None,
            "payTypes": [],
            "classifies": [
                "mass",
                "profession",
                "fiat_trade"
            ],
            "tradedWith": False,
            "followed": False,
            "periods": [],
            "filterType": "tradable",
            "additionalKycVerifyFilter": 0
        }
    },
    {
        # Продать USDT за VND
        "change_type": 3,
        "payload": {
            "fiat": "VND",
            "page": 1,
            "rows": 25,
            "tradeType": "SELL",
            "asset": "USDT",
            "countries": [],
            "proMerchantAds": False,
            "shieldMerchantAds": False,
            "publisherType": None,
            "payTypes": [],
            "classifies": [
                "mass",
                "profession",
                "fiat_trade"
            ],
            "tradedWith": False,
            "followed": False,
            "periods": [],
            "filterType": "tradable",
            "additionalKycVerifyFilter": 0
        }
    }
]


def required_env(name):
    value = os.environ.get(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

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
            INSERT INTO raw_data.load_error_log
            (
                load_id,
                error_description
            )
            VALUES (%s, %s)
            """,
            (
                load_id,
                error_description
            )
        )


conn = psycopg2.connect(
    dbname=required_env("DB_NAME"),
    user=required_env("DB_USER"),
    password=required_env("DB_PASSWORD"),
    host=required_env("DB_HOST"),
    port=required_env("DB_PORT")
)

session = requests.Session()

while True:

    for market in markets:

        change_type = market["change_type"]
        payload = market["payload"]

        try:

            response = session.post(
                URL,
                json=payload,
                headers=headers,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            if data.get("code") != "000000":

                error_text = (
                    f"API ERROR change_type={change_type}: "
                    f"code={data.get('code')}"
                )

                log_error(conn, 3, error_text)

                conn.commit()

                print(error_text)

                continue

            items = data.get("data", [])

            if not items:

                print(
                    f"No items for change_type={change_type}"
                )

                continue

            rows = []

            for item in items:

                try:

                    adv = item.get("adv", {})
                    advertiser = item.get("advertiser", {})

                    seller = advertiser.get(
                        "nickName",
                        "unknown"
                    )

                    price = float(
                        adv.get("price", 0)
                    )

                    min_limit = float(
                        adv.get(
                            "minSingleTransAmount",
                            0
                        )
                    )

                    max_limit = float(
                        adv.get(
                            "dynamicMaxSingleTransAmount",
                            adv.get(
                                "maxSingleTransAmount",
                                0
                            )
                        )
                    )

                    payments = [
                        p.get("tradeMethodName")
                        for p in adv.get(
                            "tradeMethods",
                            []
                        )
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

                    error_text = (
                        f"PARSE ERROR "
                        f"change_type={change_type}: "
                        f"{parse_error}"
                    )

                    log_error(conn, 3, error_text)

                    conn.commit()

                    print(error_text)

            if not rows:

                print(
                    f"No parsed rows "
                    f"for change_type={change_type}"
                )

                continue

            with conn.cursor() as cur:

                cur.execute(
                    """
                    INSERT INTO raw_data.load_info
                    (load_type)
                    VALUES (3)
                    RETURNING id
                    """
                )

                load_id = cur.fetchone()[0]

                execute_values(
                    cur,
                    """
                    INSERT INTO raw_data.data_binance
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
                        (
                            change_type,
                            s,
                            p,
                            mn,
                            mx,
                            pay,
                            load_id
                        )
                        for s, p, mn, mx, pay in rows
                    ]
                )

            conn.commit()

            print(
                f"Success insert "
                f"change_type={change_type}, "
                f"rows={len(rows)}"
            )

        except Exception as e:

            conn.rollback()

            error_text = (
                f"ERROR change_type={change_type}: {e}"
            )

            try:

                log_error(
                    conn,
                    3,
                    error_text
                )

                conn.commit()

            except Exception as log_error_exc:

                conn.rollback()

                print(
                    f"LOG ERROR "
                    f"change_type={change_type}: "
                    f"{log_error_exc}"
                )

            print(error_text)

    time.sleep(90)