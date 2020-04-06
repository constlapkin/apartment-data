import tkinter as tk
import sqlite3
from datetime import datetime
import os.path


DB_NAME = "db.sqlite3"


def init(conn, cursor):
    cursor.execute("CREATE TABLE hot_water_data "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "value TEXT NOT NULL,"
                   "date TEXT NOT NULL)")
    conn.commit()

    cursor.execute("CREATE TABLE cold_water_data "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "value TEXT NOT NULL,"
                   "date TEXT NOT NULL)")
    conn.commit()

    cursor.execute("CREATE TABLE electricity_data "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "value TEXT NOT NULL,"
                   "date TEXT NOT NULL)")
    conn.commit()


def dbconn():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return (conn, cursor)


def dbclose(conn):
    conn.close()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.b_insert_hot_water = tk.Button(self, text="Insert Hot", width=12,
                                         command=lambda: self.new_window_hot(InsertWindow))
        self.b_insert_hot_water.grid(row=0, column=1, sticky=tk.N+tk.S, padx=3, pady=3)
        self.b_insert_cold_water = tk.Button(self, text="Insert Cold", width=12,
                                          command=lambda: self.new_window_cold(InsertWindow))
        self.b_insert_cold_water.grid(row=1, column=1, sticky=tk.N+tk.S, padx=3, pady=3)
        self.b_insert_electricity = tk.Button(self, text="Insert Electricity", width=12,
                                           command=lambda: self.new_window_electricity(InsertWindow))
        self.b_insert_electricity.grid(row=3, column=1, sticky=tk.N+tk.S, padx=3, pady=3)

    def new_window_hot(self, _class):
        self.target = "hot"
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("Insert Data")
        # self.newWindow.geometry("250x75")
        self.newWindow.resizable(width=False, height=False)
        _class(self.newWindow, self.conn, self.cursor, self.target)

    def new_window_cold(self, _class):
        self.target = "cold"
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("Insert Data")
        # self.newWindow.geometry("250x75")
        self.newWindow.resizable(width=False, height=False)
        _class(self.newWindow, self.conn, self.cursor, self.target)

    def new_window_electricity(self, _class):
        self.target = "electricity"
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("Insert Data")
        # self.newWindow.geometry("250x75")
        self.newWindow.resizable(width=False, height=False)
        _class(self.newWindow, self.conn, self.cursor, self.target)


class InsertWindow(tk.Frame):
    def __init__(self, master=None, conn=None, cursor=None, target=None):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.target = target
        self.grid()
        self.data = list()
        self.b_insert = tk.Button(self, text="Enter", width=12)
        if self.target == "hot":
            self.b_insert["command"] = lambda: self.db_insert_hot_water()
        elif self.target == "cold":
            self.b_insert["command"] = lambda: self.db_insert_cold_water()
        elif self.target == "electricity":
            self.b_insert["command"] = lambda: self.db_insert_electricity()
        self.b_insert.grid(row=0, padx=3, pady=3)
        self.inbox = tk.Entry(self)
        self.inbox.grid(row=0, column=1, padx=3, pady=3)

    def db_insert_hot_water(self):
        try:
            self.tmp = float(self.inbox.get())
        except ValueError:
            self.errorLabel = tk.Label(self, text="Error, enter right digit")
            self.errorLabel.grid(row=1, columnspan=2)
            return 0
        self.data.append(str(self.tmp))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO hot_water_data (value, date) VALUES (?, ?)", self.data)
        self.conn.commit()
        self.master.destroy()

    def db_insert_cold_water(self):
        try:
            self.tmp = float(self.inbox.get())
        except ValueError:
            self.errorLabel = tk.Label(self, text="Error, enter right digit")
            self.errorLabel.grid(row=1, columnspan=2)
            return 0
        self.data.append(str(self.tmp))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO cold_water_data (value, date) VALUES (?, ?)", self.data)
        self.conn.commit()
        self.master.destroy()

    def db_insert_electricity(self):
        try:
            self.tmp = float(self.inbox.get())
        except ValueError:
            self.errorLabel = tk.Label(self, text="Error, enter right digit")
            self.errorLabel.grid(row=1, columnspan=2)
            return 0
        self.data.append(str(self.tmp))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO electricity_data (value, date) VALUES (?, ?)", self.data)
        self.conn.commit()
        self.master.destroy()


def gui_main():

    if not os.path.exists(DB_NAME):
        conn, cursor = dbconn()
        init(conn, cursor)
        dbclose(conn)


    root = tk.Tk()
    root.title("Utility Cost Data")
    root.resizable(width=False, height=False)
    # root.geometry("300x100")
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    gui_main()
