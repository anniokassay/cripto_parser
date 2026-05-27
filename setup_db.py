import psycopg2

conn = psycopg2.connect(
    dbname="dwh",
    user="bybitparser",
    password="TokenPWforByBit",
    host="46.21.81.183",
    port="5432",
)
with conn.cursor() as cur:
    cur.execute("SELECT current_user, current_database()")
    print("Connected as:", cur.fetchone())
    cur.execute(
        """
        SELECT schema_name FROM information_schema.schemata
        WHERE schema_name = 'row_data'
        """
    )
    print("row_data schema:", cur.fetchone())
    cur.execute(
        """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY 1, 2
        """
    )
    print("Tables:", cur.fetchall())
conn.close()
print("Schema and table ready.")
