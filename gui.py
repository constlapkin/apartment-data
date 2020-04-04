from tkinter import *
import sqlite3
from datetime import datetime


DB_NAME = "db.sqlite3"


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.b_insert_hot_water = Button(self, text="Insert Hot", command=lambda: self.new_window_hot(InsertWindow))
        self.b_insert_hot_water.pack()
        self.b_insert_cold_water = Button(self, text="Insert Cold", command=lambda: self.new_window_cold(InsertWindow))
        self.b_insert_cold_water.pack()
        self.b_insert_electricity = Button(self, text="Insert Electricity", command=lambda: self.new_window_electricity(InsertWindow))
        self.b_insert_electricity.pack()

    def new_window_hot(self, _class):
        self.target = "hot"
        self.newWindow = Toplevel(self.master)
        _class(self.newWindow, self.conn, self.cursor, self.target)

    def new_window_cold(self, _class):
        self.target = "cold"
        self.newWindow = Toplevel(self.master)
        _class(self.newWindow, self.conn, self.cursor, self.target)

    def new_window_electricity(self, _class):
        self.target = "electricity"
        self.newWindow = Toplevel(self.master)
        _class(self.newWindow, self.conn, self.cursor, self.target)


class InsertWindow(Frame):
    def __init__(self, master=None, conn=None, cursor=None, target=None):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.target = target
        self.pack()
        self.data = list()
        self.l = Label(master, text="Hello, world!")
        self.l.pack()
        self.inbox = Entry(master)
        self.inbox.pack()
        self.b_insert = Button(self, text="Enter")
        if self.target == "hot":
            self.b_insert["command"] = lambda: self.db_insert_hot_water()
        elif self.target == "cold":
            self.b_insert["command"] = lambda: self.db_insert_cold_water()
        elif self.target == "electricity":
            self.b_insert["command"] = lambda: self.db_insert_electricity()
        self.b_insert.pack()

    def db_insert_hot_water(self):
        self.data.append(str(float(self.inbox.get())))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO hot_water_data (value, date) VALUES (?, ?)", self.data)
        self.conn.commit()

    def db_insert_cold_water(self):
        self.data.append(str(float(self.inbox.get())))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO cold_water_data (value, date) VALUES (?, ?)", self.data)
        self.conn.commit()

    def db_insert_electricity(self):
        self.data.append(str(float(self.inbox.get())))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO electricity_data (value, date) VALUES (?, ?)", self.data)
        self.conn.commit()


def gui_main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()



if __name__ == "__main__":
    gui_main()