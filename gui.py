import tkinter as tk
import sqlite3
from datetime import datetime
import os.path


DB_NAME = "db.sqlite3"

ORDER_TABLE = "DESC"
LIMIT_TABLE = "10"

HOT_WATER_TABLE = "hot_water_data"
COLD_WATER_TABLE = "cold_water_data"
ELECTRICITY_TABLE = "electricity_data"

HOT_WATER_TARGET = "hot"
COLD_WATER_TARGET = "cold"
ELECTRICITY_TARGET = "electricity"


def init(conn, cursor):
    cursor.execute("CREATE TABLE {0} "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "value TEXT NOT NULL,"
                   "date TEXT NOT NULL)".format(HOT_WATER_TABLE))
    conn.commit()

    cursor.execute("CREATE TABLE {0} "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "value TEXT NOT NULL,"
                   "date TEXT NOT NULL)".format(COLD_WATER_TABLE))
    conn.commit()

    cursor.execute("CREATE TABLE {0} "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "value TEXT NOT NULL,"
                   "date TEXT NOT NULL)".format(ELECTRICITY_TABLE))
    conn.commit()


def dbconn():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return (conn, cursor)


def dbclose(conn):
    conn.close()


class Table(tk.Frame):
    def __init__(self, master, data=(())):
        tk.Frame.__init__(self, master)
        self.rows = len(data)
        self.columns = len(data[0])

        for row in range(self.rows):
            for column in range(self.columns):
                self.cell = tk.Label(self, text="%s" % (data[row][column]), relief=tk.SUNKEN, borderwidth=1,
                                     bg="white", width=13, anchor=tk.W)

                # value_var = tk.StringVar()
                # value_var.set(str(data[row][column]))
                # self.cell = tk.Entry(self, state="readonly", textvariable=value_var, width=13)

#                if column == 1:
#                    self.cell.bind("<Button-1>", self.label_bind)

                self.cell.grid(row=row, column=column, padx=1, pady=1)

# don't know, but it's working
#    def label_bind(self, *args):
#        self.aae = tk.Label(self, text="ssaxca")
#        self.aae.grid(row=0)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

        # connect
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        # show data
        self.data = self.cursor.execute("SELECT date, value FROM {0} "
                                        "ORDER BY id {1} "
                                        "LIMIT {2}".format(HOT_WATER_TABLE, ORDER_TABLE, LIMIT_TABLE)).fetchall()
        self.table_hot = Table(self, self.data)
        self.table_hot.grid(row=0, column=0, rowspan=3, sticky=tk.W, padx=3, pady=3)
        self.data = self.cursor.execute("SELECT date, value FROM {0} "
                                        "ORDER BY id {1} "
                                        "LIMIT {2}".format(COLD_WATER_TABLE, ORDER_TABLE, LIMIT_TABLE)).fetchall()
        self.table_cold = Table(self, self.data)
        self.table_cold.grid(row=0, column=1, rowspan=3, sticky=tk.W, padx=3, pady=3)
        self.data = self.cursor.execute("SELECT date, value FROM {0} "
                                        "ORDER BY id {1} "
                                        "LIMIT {2}".format(ELECTRICITY_TABLE, ORDER_TABLE, LIMIT_TABLE)).fetchall()
        self.table_electricity = Table(self, self.data)
        self.table_electricity.grid(row=0, column=2, rowspan=3, sticky=tk.W, padx=3, pady=3)

        # insert data
        self.exist_insert_window = False
        self.b_insert_hot_water = tk.Button(self, text="Insert Hot", width=12,
                                            command=lambda: self.new_window_insert(InsertWindow, HOT_WATER_TARGET))
        self.b_insert_hot_water.grid(row=0, column=3, sticky=tk.E, padx=3, pady=3)
        self.b_insert_cold_water = tk.Button(self, text="Insert Cold", width=12,
                                             command=lambda: self.new_window_insert(InsertWindow, COLD_WATER_TARGET))
        self.b_insert_cold_water.grid(row=1, column=3, sticky=tk.E, padx=3, pady=3)
        self.b_insert_electricity = tk.Button(self, text="Insert Electricity", width=12,
                                              command=lambda: self.new_window_insert(InsertWindow, ELECTRICITY_TARGET))
        self.b_insert_electricity.grid(row=2, column=3, sticky=tk.E, padx=3, pady=3)

    def update_table(self, type):
        data = self.cursor.execute("SELECT date, value FROM {0} ORDER BY id DESC LIMIT 10".format(type)).fetchall()
        self.table = Table(self, data)
        tmp_column = -1
        if type == HOT_WATER_TABLE:
            tmp_column = 0
        elif type == COLD_WATER_TABLE:
            tmp_column = 1
        elif type == ELECTRICITY_TABLE:
            tmp_column = 2
        if tmp_column >= 0:
            self.table.grid(row=0, column=tmp_column, rowspan=3, sticky=tk.W, padx=3, pady=3)
        self.exist_insert_window = False

    def delete_insert_window(self):
        self.exist_insert_window = False
        self.newWindow.destroy()

    def new_window_insert(self, _class, target):
        if self.exist_insert_window is not True:
            self.newWindow = tk.Toplevel(self.master)
            self.newWindow.title("Insert Data")
            # self.newWindow.geometry("250x75")
            self.newWindow.resizable(width=False, height=False)
            self.newWindow.protocol("WM_DELETE_WINDOW", self.delete_insert_window)
            _class(self.newWindow, self.conn, self.cursor, target, self)
            self.exist_insert_window = True


class InsertWindow(tk.Frame):
    def __init__(self, master=None, conn=None, cursor=None, target=None, obj=None):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.target = target
        self.grid()
        self.data = list()
        self.b_insert = tk.Button(self, text="Enter", width=12)
        if self.target == HOT_WATER_TARGET:
            type_insert = HOT_WATER_TABLE
            self.b_insert["command"] = lambda: self.db_insert_data(obj, type_insert)
        elif self.target == COLD_WATER_TARGET:
            type_insert = COLD_WATER_TABLE
            self.b_insert["command"] = lambda: self.db_insert_data(obj, type_insert)
        elif self.target == ELECTRICITY_TARGET:
            type_insert = ELECTRICITY_TABLE
            self.b_insert["command"] = lambda: self.db_insert_data(obj, type_insert)
        self.b_insert.grid(row=0, padx=3, pady=3)
        self.inbox = tk.Entry(self)
        self.inbox.grid(row=0, column=1, padx=3, pady=3)
        self.inbox.focus()

    def validation_insert(self, type):
        try:
            self.tmp_value = float(self.inbox.get())
        except ValueError:
            self.errorLabel = tk.Label(self, text="Error, enter right digit")
            self.errorLabel.grid(row=1, columnspan=2)
            return False
        self.tmp_value_old = float(self.cursor.execute("SELECT value FROM {0} ORDER BY id DESC LIMIT 1".format(type)).fetchone()[0])
        if self.tmp_value_old >= self.tmp_value:
            self.errorLabel = tk.Label(self, text="Error, too small value")
            self.errorLabel.grid(row=1, columnspan=2)
            return False
        return True

    def db_insert_data(self, obj, type):
        if self.validation_insert(type) is False:
            return 0
        self.data.append(str(self.tmp_value))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO {0} (value, date) VALUES (?, ?)".format(type), self.data)
        self.conn.commit()
        obj.update_table(type)
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
