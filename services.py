# services.py
from db import get_conn
from datetime import datetime
import random

# ---------- Helpers ----------
def _now():
    return datetime.now().isoformat(sep=' ', timespec='seconds')

def _generate_acc_no():
    # Example: 10-digit starting with 1001...
    return str(1000000000 + random.randint(0, 899999999))

# ---------- Customer CRUD ----------
def create_customer(name, phone, email, address, initial_balance=0.0):
    conn = get_conn(); cur = conn.cursor()
    # ensure unique acc_no
    acc_no = _generate_acc_no()
    # try until unique
    while True:
        cur.execute("SELECT 1 FROM customers WHERE acc_no=?", (acc_no,))
        if cur.fetchone() is None:
            break
        acc_no = _generate_acc_no()
    cur.execute("""INSERT INTO customers(acc_no,name,phone,email,address,balance)
                   VALUES (?,?,?,?,?,?)""", (acc_no, name, phone, email, address, initial_balance))
    cid = cur.lastrowid
    # create initial transaction if balance > 0
    if initial_balance and initial_balance > 0:
        now = _now()
        cur.execute("""INSERT INTO transactions(cust_id,txn_type,amount,details,created_at)
                       VALUES (?,?,?,?,?)""", (cid, 'deposit', initial_balance, 'Opening balance', now))
    conn.commit(); conn.close()
    return {'id': cid, 'acc_no': acc_no}

def get_customers():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM customers ORDER BY id DESC")
    rows = cur.fetchall(); conn.close(); return rows

def get_customer_by_id(cid):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE id=?", (cid,))
    r = cur.fetchone(); conn.close(); return r

def get_customer_by_acc(acc_no):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE acc_no=?", (acc_no,))
    r = cur.fetchone(); conn.close(); return r

# ---------- Transactions ----------
def add_transaction(cust_id, txn_type, amount, details=""):
    conn = get_conn(); cur = conn.cursor()
    now = _now()
    cur.execute("""INSERT INTO transactions(cust_id,txn_type,amount,details,created_at)
                   VALUES (?,?,?,?,?)""", (cust_id, txn_type, amount, details, now))
    conn.commit(); conn.close()

def deposit(cust_id, amount, details=""):
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE customers SET balance = balance + ? WHERE id=?", (amount, cust_id))
    add_transaction(cust_id, "deposit", amount, details or "Deposit")
    conn.close()

def withdraw(cust_id, amount, details=""):
    if amount <= 0:
        raise ValueError("Withdraw amount must be positive")
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT balance FROM customers WHERE id=?", (cust_id,))
    row = cur.fetchone()
    if row is None:
        conn.close(); raise ValueError("Customer not found")
    if row["balance"] < amount:
        conn.close(); raise ValueError("Insufficient balance")
    cur.execute("UPDATE customers SET balance = balance - ? WHERE id=?", (amount, cust_id))
    add_transaction(cust_id, "withdraw", amount, details or "Withdraw")
    conn.close()

def transfer(src_id, dst_id, amount):
    if src_id == dst_id:
        raise ValueError("Source and destination cannot be same")
    # atomic-ish: do checks then update
    withdraw(src_id, amount, f"Transfer to {dst_id}")
    deposit(dst_id, amount, f"Transfer from {src_id}")
    # add_transaction already called inside withdraw/deposit

def get_transactions(cust_id):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE cust_id=? ORDER BY id DESC", (cust_id,))
    rows = cur.fetchall(); conn.close(); return rows
