from flask import Flask
import os
import psycopg2

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dbname=os.environ["DB_NAME"],
    )


@app.route("/add")
def add_order():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY)")
    cur.execute("INSERT INTO orders DEFAULT VALUES")
    conn.commit()
    cur.close()
    conn.close()
    return "order added"


@app.route("/count")
def count_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM orders")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return str(count)


app.run(host="0.0.0.0", port=8000)
