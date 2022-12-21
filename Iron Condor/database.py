import os
import sqlite3

db_path = 'ic.db'

query = '''create table orders (
    o_id        INTEGER primary key,
    symbol        text,
    leg           text,
    strike_price  INTEGER,
    price         INTEGER,
    spot_price    INTEGER,
    date_time    TIMESTAMP
)'''


def check_db_exist():
    db_exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    is_db_exist = False
    if db_exists:
        print('Database exists...')
        is_db_exist = True
    else:
        print("Database does not exists, create a new database.")
    conn.close()
    return is_db_exist


def create_orders():
    db_exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if db_exists:
        cur = conn.cursor()
        obj = cur.execute(query)
        conn.commit()
        if obj.arraysize == 1:
            print("orders table created successfully...", obj.arraysize)
            return obj.arraysize
        else:
            return 0
    else:
        print("Database does not exists, create a new database.")
    conn.close()


# def insert_data(order_list):
def insert_data(order_list):
    db_exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if db_exists:
        cur = conn.cursor()
        pp = cur.executemany("insert into orders values (?, ?, ?, ?, ?, ? ,?)", order_list)
        conn.commit()
        print("Record inserted successfully...", pp)
    else:
        print("Database does not exists, create a new database.")
    conn.close()


def fetch_data():
    db_exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if db_exists:
        cur = conn.cursor()
        cur.execute("select * from orders")
        records = cur.fetchall()

        print("Fetching all records from orders table")
        print("\n", records)
    else:
        print("Database does not exists, create a new database.")
    conn.close()
