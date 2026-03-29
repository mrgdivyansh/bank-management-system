from db import init_db, get_conn
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import random, re

# ---------------- VALIDATION ----------------
def valid_email(email): return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)
def valid_phone(p): return p.isdigit() and len(p)==10
def valid_aadhar(a): return a.isdigit() and len(a)==12

def popup(msg):
    tb.Messagebox.show_info(title="Info", message=msg)

# ---------------- CENTER WINDOW ----------------
def center_window(win, width, height):
    win.update_idletasks()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# ---------------- STYLES ----------------
BTN_STYLE = {"width": 25}
ENTRY_STYLE = {"width": 30}
FONT_TITLE = ("Calibri", 22, "bold")
FONT_LABEL = ("Calibri", 12)

# ---------------- MAIN ----------------
def main_screen():
    root = tb.Window(themename="cyborg")
    root.title("Bank System")
    center_window(root, 600, 400)

    # 🔥 Better card (no pure black)
    card = tb.Frame(root, bootstyle="primary", padding=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tb.Label(card, text="🏦 Bank Management System", font=FONT_TITLE).pack(pady=20)

    tb.Button(card, text="Admin Login", bootstyle="danger", **BTN_STYLE,
              command=lambda: open_login("Admin")).pack(pady=10)

    tb.Button(card, text="Customer Login", bootstyle="success", **BTN_STYLE,
              command=lambda: open_login("Customer")).pack(pady=10)

    tb.Button(card, text="Create Account", bootstyle="info", **BTN_STYLE,
              command=choose_account_type).pack(pady=10)

    root.mainloop()

# ---------------- ACCOUNT TYPE ----------------
def choose_account_type():
    win = tb.Toplevel()
    win.title("Select Account Type")
    center_window(win, 350, 250)

    card = tb.Frame(win, bootstyle="info", padding=25)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tb.Label(card, text="Are you?", font=FONT_TITLE).pack(pady=20)

    tb.Button(card, text="Admin", bootstyle="danger", **BTN_STYLE,
              command=lambda: open_create_admin(win)).pack(pady=10)

    tb.Button(card, text="Customer", bootstyle="success", **BTN_STYLE,
              command=lambda: open_create_customer(win)).pack(pady=10)

# ---------------- CREATE ADMIN ----------------
def open_create_admin(prev):
    prev.destroy()
    win = tb.Toplevel()
    win.title("Create Admin")
    center_window(win, 400, 500)

    card = tb.Frame(win, bootstyle="info", padding=25)
    card.place(relx=0.5, rely=0.5, anchor="center")

    fields = {}
    for label in ["Name","Email","Phone","Aadhar","Password"]:
        tb.Label(card, text=label, font=FONT_LABEL).pack()
        entry = tb.Entry(card, **ENTRY_STYLE, show="*" if label=="Password" else "")
        entry.pack(pady=6)
        fields[label] = entry

    def save():
        if not valid_email(fields["Email"].get()): return popup("Invalid Email")
        if not valid_phone(fields["Phone"].get()): return popup("Invalid Phone")
        if not valid_aadhar(fields["Aadhar"].get()): return popup("Invalid Aadhar")

        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO admins(username,password) VALUES(?,?)",
                    (fields["Email"].get(), fields["Password"].get()))
        conn.commit(); conn.close()
        popup("Admin Created")

    tb.Button(card, text="Create", bootstyle="success", width=25,
              command=save).pack(pady=15)

# ---------------- CREATE CUSTOMER ----------------
def open_create_customer(prev):
    prev.destroy()
    win = tb.Toplevel()
    win.title("Create Customer")
    center_window(win, 400, 600)

    card = tb.Frame(win, bootstyle="info", padding=25)
    card.place(relx=0.5, rely=0.5, anchor="center")

    labels = ["Name","Email","Phone","Aadhar","Age","Address","Password"]
    fields = {}

    for label in labels:
        tb.Label(card, text=label, font=FONT_LABEL).pack()
        entry = tb.Entry(card, **ENTRY_STYLE, show="*" if label=="Password" else "")
        entry.pack(pady=6)
        fields[label] = entry

    def save():
        if not valid_email(fields["Email"].get()): return popup("Invalid Email")
        if not valid_phone(fields["Phone"].get()): return popup("Invalid Phone")
        if not valid_aadhar(fields["Aadhar"].get()): return popup("Invalid Aadhar")

        acc_no = str(random.randint(100000,999999))
        conn = get_conn(); cur = conn.cursor()

        cur.execute("INSERT INTO customers(acc_no,name,email,phone,aadhar,address,balance) VALUES(?,?,?,?,?,?,?)",
                    (acc_no, fields["Name"].get(), fields["Email"].get(),
                     fields["Phone"].get(), fields["Aadhar"].get(),
                     fields["Address"].get(), 0))

        conn.commit(); conn.close()
        popup(f"Customer Created\nAcc No: {acc_no}")

    tb.Button(card, text="Create", bootstyle="success", width=25,
              command=save).pack(pady=15)

# ---------------- LOGIN ----------------
def open_login(user_type):
    win = tb.Toplevel()
    win.title(f"{user_type} Login")
    center_window(win, 350, 250)

    card = tb.Frame(win, bootstyle="info", padding=25)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tb.Label(card, text=f"{user_type} Login", font=FONT_TITLE).pack(pady=15)

    user = tb.Entry(card, **ENTRY_STYLE)
    pwd = tb.Entry(card, **ENTRY_STYLE, show="*")

    tb.Label(card, text="Username / AccNo").pack()
    user.pack(pady=5)

    tb.Label(card, text="Password").pack()
    pwd.pack(pady=5)

    def login():
        conn = get_conn(); cur = conn.cursor()
        if user_type=="Admin":
            cur.execute("SELECT * FROM admins WHERE username=? AND password=?", (user.get(), pwd.get()))
        else:
            cur.execute("SELECT * FROM customers WHERE acc_no=? AND password=?", (user.get(), pwd.get()))
        if cur.fetchone(): popup("Login Success")
        else: popup("Invalid Credentials")
        conn.close()

    tb.Button(card, text="Login", width=25, bootstyle="primary",
              command=login).pack(pady=15)

# ---------------- ENTRY ----------------
if __name__ == "__main__":
    init_db()

    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM admins WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO admins(username,password) VALUES('admin','1234')")
        conn.commit()
    conn.close()

    main_screen()
