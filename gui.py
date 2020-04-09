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
    """
    Creating tables for empty database
    :param conn: Connection object database
    :param cursor: Cursor object database
    :return:
    """
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
    """
    Create sqlite3 database. Initialize connection and cursor for sqlite3 database
    :return (conn, cursor):
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return (conn, cursor)


def dbclose(conn):
    """
    Close database connection
    :param conn: Connection object database
    :return:
    """
    conn.close()


class Table(tk.Frame):
    """
    Class for table widget. It's creating label-based table.
    :param master: It's object tkinter
    :param data: Data would be insert into table
    :param target: Target table for edit in database
    :param conn: Connection object database
    :param cursor: Cursor object database
    :return:
    """
    def __init__(self, master=None, data=(()), target=None, conn=None, cursor=None):
        tk.Frame.__init__(self, master)
        self.exist_edit_window = False
        self.rows = len(data)
        self.conn = conn
        self.cursor = cursor
        if len(data) != 0:
            self.columns = len(data[0])
        self.cell = [[0]*2]*len(data)
        for row in range(self.rows):
            for column in range(self.columns):
                if column == 0:
                    id = data[row][column]
                    continue
                self.cell[row][column-1] = tk.Label(self, text="%s" % (data[row][column]),
                                                    relief=tk.SUNKEN, borderwidth=1,
                                                    bg="white", width=13, anchor=tk.W)
                if column == 2:
                    self.cell[row][column-1].bind("<Button-1>",
                                                  lambda x, id=id:self.new_window_edit(InsertWindow,
                                                                                       master, target, id))
                self.cell[row][column-1].grid(row=row, column=column, padx=1, pady=1)

    def new_window_edit(self, _class, master, target, id, *args):
        """
        Create window for edit data
        :param _class: class new window
        :param master: main object tkinter
        :param target:
        :param id: id row in database
        :param args: for bind (event)
        :return:
        """
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("Edit Data")
        self.newWindow.resizable(width=False, height=False)
        command = "E"
        _class(self.newWindow, master, command, self.conn, self.cursor, target, id)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

        # connect
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        # show data
        self.data = self.cursor.execute("SELECT id, date, value FROM {0} "
                                        "ORDER BY id {1} "
                                        "LIMIT {2}".format(HOT_WATER_TABLE, ORDER_TABLE, LIMIT_TABLE)).fetchall()
        self.table_hot = Table(self, self.data, HOT_WATER_TARGET, self.conn, self.cursor)
        self.table_hot.grid(row=0, column=0, rowspan=3, sticky=tk.W, padx=3, pady=3)
        self.data = self.cursor.execute("SELECT id, date, value FROM {0} "
                                        "ORDER BY id {1} "
                                        "LIMIT {2}".format(COLD_WATER_TABLE, ORDER_TABLE, LIMIT_TABLE)).fetchall()
        self.table_cold = Table(self, self.data, COLD_WATER_TARGET, self.conn, self.cursor)
        self.table_cold.grid(row=0, column=1, rowspan=3, sticky=tk.W, padx=3, pady=3)
        self.data = self.cursor.execute("SELECT id, date, value FROM {0} "
                                        "ORDER BY id {1} "
                                        "LIMIT {2}".format(ELECTRICITY_TABLE, ORDER_TABLE, LIMIT_TABLE)).fetchall()
        self.table_electricity = Table(self, self.data, ELECTRICITY_TARGET, self.conn, self.cursor)
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
        """
        Initialize update table after commit changes or inserting data
        :param type:
        :return:
        """
        data = self.cursor.execute("SELECT id, date, value FROM {0} ORDER BY id DESC LIMIT 10".format(type)).fetchall()
        if type == HOT_WATER_TABLE:
            target = HOT_WATER_TARGET
        elif type == COLD_WATER_TABLE:
            target = COLD_WATER_TARGET
        elif type == ELECTRICITY_TABLE:
            target = ELECTRICITY_TARGET
        self.table = Table(self, data, target, self.conn, self.cursor)
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
        """
        Changes flag for creating only one window.
        Destroyed window
        :return:
        """
        self.exist_insert_window = False
        self.newWindow.destroy()

    def new_window_insert(self, _class, target):
        """
        Create window for insert data
        :param _class:
        :param target:
        :return:
        """
        if self.exist_insert_window is not True:
            self.newWindow = tk.Toplevel(self.master)
            self.newWindow.title("Insert Data")
            # self.newWindow.geometry("250x75")
            self.newWindow.resizable(width=False, height=False)
            self.newWindow.protocol("WM_DELETE_WINDOW", self.delete_insert_window)
            command = "I"
            _class(self.newWindow, self, command, self.conn, self.cursor, target)
            self.exist_insert_window = True


class InsertWindow(tk.Frame):
    """
    Creating new window for edit or insert new data to database.
    :param master:
    :param obj: main object tkinter
    :param command: for define type of operation - insert or edit ("I" / "E")
    :param conn:
    :param cursor:
    :param target:
    :param id: only for edit data
    :return:
    """
    def __init__(self, master=None, obj=None, command="I", conn=None, cursor=None, target=None, id=None):
        super().__init__(master)
        self.master = master
        if conn is None or cursor is None and obj is not None:
            self.conn = obj.conn
            self.cursor = obj.cursor
        else:
            self.conn = conn
            self.cursor = cursor
        self.target = target
        self.grid()
        self.data = list()
        self.b_insert = tk.Button(self, text="Enter", width=12)
        if self.target == HOT_WATER_TARGET:
            table = HOT_WATER_TABLE
            if command == "I":
                self.b_insert["command"] = lambda: self.db_insert_data(obj, table)
            elif command == "E":
                self.b_insert["command"] = lambda: self.db_edit_data(obj, table, id)
        elif self.target == COLD_WATER_TARGET:
            table = COLD_WATER_TABLE
            if command == "I":
                self.b_insert["command"] = lambda: self.db_insert_data(obj, table)
            elif command == "E":
                self.b_insert["command"] = lambda: self.db_edit_data(obj, table, id)
        elif self.target == ELECTRICITY_TARGET:
            table = ELECTRICITY_TABLE
            if command == "I":
                self.b_insert["command"] = lambda: self.db_insert_data(obj, table)
            elif command == "E":
                self.b_insert["command"] = lambda: self.db_edit_data(obj, table, id)
        self.b_insert.grid(row=0, padx=3, pady=3)
        self.inbox = tk.Entry(self)
        self.inbox.grid(row=0, column=1, padx=3, pady=3)
        self.inbox.focus()

    def validation_insert(self, table):
        """
        Validate insert data (by type and value)
        :param table:
        :return:
        """
        try:
            self.tmp_value = float(self.inbox.get())
        except ValueError:
            self.errorLabel = tk.Label(self, text="Error, enter right digit")
            self.errorLabel.grid(row=1, columnspan=2)
            return False
        try:
            self.tmp_value_old = float(self.cursor.execute("SELECT value FROM {0} "
                                                           "ORDER BY id DESC LIMIT 1".format(table)).fetchone()[0])
        except TypeError:
            self.tmp_value_old = 0

        if self.tmp_value_old >= self.tmp_value:
            self.errorLabel = tk.Label(self, text="Error, too small value")
            self.errorLabel.grid(row=1, columnspan=2)
            return False
        return True

    def validation_edit(self, table, id):
        """
        Validate edit data (by type and value)
        :param table:
        :param id:
        :return:
        """
        try:
            self.tmp_value = float(self.inbox.get())
        except ValueError:
            self.errorLabel = tk.Label(self, text="Error, enter right digit")
            self.errorLabel.grid(row=1, columnspan=2)
            return False

        try:
            self.tmp_value_up = float(self.cursor.execute("SELECT value FROM {0} WHERE id > (?) "
                                                          "ORDER BY id ASC LIMIT 1".format(table), (str(id),)).fetchone()[0])
        except TypeError:
            self.tmp_value_up = -1

        try:
            self.tmp_value_down = float(self.cursor.execute("SELECT value FROM {0} WHERE id < (?) "
                                                            "ORDER BY id DESC LIMIT 1".format(table), (str(id),)).fetchone()[0])
        except TypeError:
            self.tmp_value_down = -1

        if self.tmp_value_up == -1 and (self.tmp_value_down == -1 or self.tmp_value_down < self.tmp_value) \
                or self.tmp_value_down == -1 and self.tmp_value_up > self.tmp_value \
                or self.tmp_value_down < self.tmp_value < self.tmp_value_up:
            return True
        else:
            self.errorLabel = tk.Label(self, text="Error, enter small or big digit")
            self.errorLabel.grid(row=1, columnspan=2)
            return False

    def db_insert_data(self, obj, table):
        """
        Calls validation_insert function and if return True - insert data into database
        :param obj:
        :param table:
        :return:
        """
        if self.validation_insert(table) is False:
            return 0
        self.data.append(str(self.tmp_value))
        self.data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.cursor.execute("INSERT INTO {0} (value, date) VALUES (?, ?)".format(table), self.data)
        self.conn.commit()
        obj.update_table(table)
        self.master.destroy()

    def db_edit_data(self, obj, table, id):
        """
        Calls validation_edit function and if return True - edit and commit data into database
        :param obj:
        :param table:
        :param id:
        :return:
        """
        if self.validation_edit(table, id) is False:
            return 0
        self.cursor.execute("UPDATE {0} SET value = (?) WHERE id = (?)".format(table), (str(self.tmp_value), id))
        self.conn.commit()
        obj.update_table(table)
        self.master.destroy()



def gui_main():
    # TODO:
    #  Make rows deletable
    #  Отбить переменную проверку созданного окна
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
