import os
import time
import psycopg2

from playwright.sync_api import sync_playwright
from psycopg2.extras import Json, execute_values

URL = "https://www.gate.com/api/web/v1/c2c/advertisements?sub_website_id=0"

c_load_type = 4

markets = [
    {
        "change_type": 1,  # BUY USDT / RUB
        "payload": {
            "type": "push_order_list",
            "asset_pair": "USDT_RUB",
            "push_type": "sell",
            "page": 1,
            "per_page": 25,
            "sort_type": 1
        }
    },
    {
        "change_type": 3,  # SELL USDT / VND
        "payload": {
            "type": "push_order_list",
            "asset_pair": "USDT_VND",
            "push_type": "buy",
            "page": 1,
            "per_page": 25,
            "sort_type": 1
        }
    },
    {
        "change_type": 5,  # SELL USDT / CNY
        "payload": {
            "type": "push_order_list",
            "asset_pair": "USDT_CNY",
            "push_type": "buy",
            "page": 1,
            "per_page": 25,
            "sort_type": 1
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
            INSERT INTO raw_data.load_info(load_type)
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
            VALUES (%s,%s)
            """,
            (
                load_id,
                error_description
            )
        )


def create_browser():

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        "https://www.gate.com/p2p",
        wait_until="networkidle",
        timeout=60000
    )

    return playwright, browser, page


def fetch_market(page, payload):

    return page.evaluate(
        """
        async ({url, payload}) => {

            const response = await fetch(
                url,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams(payload)
                }
            );

            return await response.json();
        }
        """,
        {
            "url": URL,
            "payload": payload
        }
    )


conn = psycopg2.connect(
    dbname=required_env("DB_NAME"),
    user=required_env("DB_USER"),
    password=required_env("DB_PASSWORD"),
    host=required_env("DB_HOST"),
    port=required_env("DB_PORT")
)

playwright = None
browser = None
page = None

while True:

    try:

        if page is None:

            playwright, browser, page = create_browser()

            print(
                "Gate browser initialized"
            )

        for market in markets:

            change_type = market["change_type"]

            payload = market["payload"]

            try:

                data = fetch_market(
                    page,
                    payload
                )

                if data.get("code") != 0:

                    error_text = (
                        f"API ERROR "
                        f"change_type={change_type}: "
                        f"code={data.get('code')}"
                    )

                    log_error(
                        conn,
                        c_load_type,
                        error_text
                    )

                    conn.commit()

                    print(error_text)

                    continue

                items = (
                    data
                    .get("data", {})
                    .get("lists", [])
                )

                if not items:

                    print(
                        f"No items "
                        f"for change_type={change_type}"
                    )

                    continue

                rows = []

                for item in items:

                    try:

                        seller = item.get(
                            "nick",
                            "unknown"
                        )

                        price = float(
                            item.get(
                                "rate",
                                0
                            )
                        )

                        min_limit = float(
                            item.get(
                                "min_amount",
                                0
                            )
                        )

                        max_limit = float(
                            item.get(
                                "max_amount",
                                0
                            )
                        )

                        payments = (
                            item.get(
                                "pay_type_num",
                                ""
                            )
                            .split(",")
                        )

                        rows.append(
                            (
                                seller,
                                price,
                                min_limit,
                                max_limit,
                                Json(payments)
                            )
                        )

                    except Exception as parse_error:

                        error_text = (
                            f"PARSE ERROR "
                            f"change_type={change_type}: "
                            f"{parse_error}"
                        )

                        log_error(
                            conn,
                            c_load_type,
                            error_text
                        )

                        conn.commit()

                        print(error_text)

                if not rows:

                    continue

                with conn.cursor() as cur:

                    cur.execute(
                        """
                        INSERT INTO raw_data.load_info
                        (
                            load_type
                        )
                        VALUES (%s)
                        RETURNING id
                        """,
                        (c_load_type,)
                    )

                    load_id = cur.fetchone()[0]

                    execute_values(
                        cur,
                        """
                        INSERT INTO raw_data.data_gatecom
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
                                seller,
                                price,
                                min_limit,
                                max_limit,
                                payments,
                                load_id
                            )
                            for (
                                seller,
                                price,
                                min_limit,
                                max_limit,
                                payments
                            ) in rows
                        ]
                    )

                conn.commit()

                print(
                    f"Success "
                    f"change_type={change_type}, "
                    f"rows={len(rows)}"
                )

            except Exception as e:

                conn.rollback()

                error_text = (
                    f"ERROR "
                    f"change_type={change_type}: "
                    f"{e}"
                )

                try:

                    log_error(
                        conn,
                        c_load_type,
                        error_text
                    )

                    conn.commit()

                except Exception:

                    conn.rollback()

                print(error_text)

        time.sleep(90)

    except Exception as browser_error:

        print(
            f"Browser restart required: "
            f"{browser_error}"
        )

        try:
            browser.close()
        except:
            pass

        try:
            playwright.stop()
        except:
            pass

        browser = None
        page = None

        time.sleep(30)