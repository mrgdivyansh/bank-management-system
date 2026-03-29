from db import init_db
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# --------------------------------------------------
# MAIN SCREEN
# --------------------------------------------------
def main_screen():
    root = tb.Window(title="Bank System", themename="solar")
    root.geometry("400x300")

    tb.Label(root, text="Select User Type", font=('Calibri', 20, 'bold')).pack(pady=20)

    tb.Button(root, text="Admin", bootstyle=PRIMARY, width=20,
              command=lambda: user_next_choice("Admin")).pack(pady=10)

    tb.Button(root, text="Customer", bootstyle=SUCCESS, width=20,
              command=lambda: user_next_choice("Customer")).pack(pady=10)

    root.mainloop()

# --------------------------------------------------
# SCREEN 2: LOGIN OR CREATE ACCOUNT
# --------------------------------------------------
def user_next_choice(user_type):
    win = tb.Toplevel()
    win.grab_set()
    win.title(f"{user_type} Options")
    win.geometry("400x250")

    tb.Label(win, text=f"{user_type} Panel", font=('Calibri', 18, 'bold')).pack(pady=20)

    tb.Button(win, text="Login", width=20,
              bootstyle=INFO,
              command=lambda: open_login(user_type, win)).pack(pady=10)

    tb.Button(win, text="Create Account", width=20,
              bootstyle=SUCCESS,
              command=lambda: open_create_account(user_type, win)).pack(pady=10)

# --------------------------------------------------
# LOGIN SCREEN
# --------------------------------------------------
def open_login(user_type, prev):
    prev.destroy()
    win = tb.Toplevel()
    win.grab_set()
    win.title(f"{user_type} Login")
    win.geometry("350x250")

    tb.Label(win, text=f"{user_type} Login", font=('Calibri', 18, 'bold')).pack(pady=20)

    username = tb.Entry(win, width=25)
    password = tb.Entry(win, width=25, show="*")
    username.pack(pady=5)
    password.pack(pady=5)

    tb.Button(win, text="Login", bootstyle=PRIMARY, width=15,
              command=lambda: open_dashboard(user_type, win)).pack(pady=10)

# --------------------------------------------------
# CREATE ACCOUNT SCREEN
# --------------------------------------------------
def open_create_account(user_type, prev):
    prev.destroy()
    win = tb.Toplevel()
    win.grab_set()
    win.title(f"{user_type} Create Account")
    win.geometry("350x300")

    tb.Label(win, text=f"{user_type} Registration", font=('Calibri', 18, 'bold')).pack(pady=20)

    name = tb.Entry(win, width=25)
    username = tb.Entry(win, width=25)
    password = tb.Entry(win, width=25, show="*")

    tb.Label(win, text="Name").pack()
    name.pack(pady=3)

    tb.Label(win, text="Username").pack()
    username.pack(pady=3)

    tb.Label(win, text="Password").pack()
    password.pack(pady=3)

    tb.Button(win, text="Create Account", bootstyle=SUCCESS, width=18,
              command=lambda: open_dashboard(user_type, win)).pack(pady=15)

# --------------------------------------------------
# POPUP WINDOW
# --------------------------------------------------
def popup_window(title, message):
    win = tb.Toplevel()
    win.grab_set()
    win.title(title)
    win.geometry("350x250")

    tb.Label(win, text=title, font=("Calibri", 18, "bold")).pack(pady=20)
    tb.Label(win, text=message, font=("Calibri", 14)).pack(pady=10)

    tb.Button(win, text="Close", width=15, bootstyle=DANGER, command=win.destroy).pack(pady=20)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
def open_dashboard(user_type, prev):
    prev.destroy()
    dash = tb.Toplevel()
    dash.grab_set()
    dash.title(f"{user_type} Dashboard")
    dash.geometry("450x420")

    tb.Label(dash, text=f"{user_type} Dashboard", font=('Calibri', 22, 'bold')).pack(pady=20)

    if user_type == "Admin":
        buttons = {
            "Open Customer Account": lambda: popup_window("Success", "Account Created Successfully!"),
            "View Statements": lambda: popup_window("Statements", "Showing customer statements..."),
            "Transactions": lambda: popup_window("Transactions", "Processing transactions..."),
            "Manage Cards": lambda: popup_window("Cards", "Cards management..."),
            "Loans": lambda: popup_window("Loans", "Loan services..."),
            "Logout": dash.destroy
        }
    else:
        buttons = {
            "My Account Details": lambda: popup_window("Account Details", "Here are your account details..."),
            "My Transactions": lambda: popup_window("My Transactions", "Showing your transactions..."),
            "My Statement": lambda: popup_window("Statement", "Generating statement..."),
            "Card Info": lambda: popup_window("Card Info", "Showing your card information..."),
            "Loan Info": lambda: popup_window("Loans", "Your loan details..."),
            "Logout": dash.destroy
        }

    for text, action in buttons.items():
        tb.Button(dash, text=text, width=25, bootstyle=INFO, command=action).pack(pady=8)

# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    init_db()
    main_screen()
