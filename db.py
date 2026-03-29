import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "bank.db"

# -----------------------------
# CONNECTION
# -----------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # ADMINS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # CUSTOMERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        acc_no TEXT UNIQUE,
        name TEXT,
        phone TEXT,
        alt_phone TEXT,
        email TEXT UNIQUE,
        aadhar TEXT,
        dob TEXT,
        address TEXT,
        balance REAL DEFAULT 0
    )
    """)

    # TRANSACTIONS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cust_id INTEGER,
        txn_type TEXT,
        amount REAL,
        details TEXT,
        created_at TEXT,
        FOREIGN KEY(cust_id) REFERENCES customers(id)
    )
    """)

    # CARDS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cust_id INTEGER,
        card_type TEXT,
        card_no TEXT UNIQUE,
        status TEXT DEFAULT 'active',
        FOREIGN KEY(cust_id) REFERENCES customers(id)
    )
    """)

    # LOANS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS loans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cust_id INTEGER,
        loan_type TEXT,
        principal REAL,
        months INTEGER,
        interest REAL,
        emi REAL,
        status TEXT DEFAULT 'ongoing',
        FOREIGN KEY(cust_id) REFERENCES customers(id)
    )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# RUN DIRECTLY
# -----------------------------
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")