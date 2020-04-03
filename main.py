import sqlite3
from datetime import datetime


ELECTRICITY_BILL = 4.51
DB_NAME = "db.sqlite3"


def dbconn():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return (conn, cursor)


def dbclose(conn):
    conn.close()


def db_select_hot(conn, cursor):
    cursor.execute("SELECT * FROM hot_water_data")
    return cursor.fetchall()


def db_select_cold(conn, cursor):
    cursor.execute("SELECT * FROM cold_water_data")
    return cursor.fetchall()


def db_select_elect(conn, cursor):
    cursor.execute("SELECT * FROM electricity_data")
    return cursor.fetchall()


def db_insert_hot(conn, cursor, data):
    cursor.execute("INSERT INTO hot_water_data (value, date) VALUES (?, ?)", data)
    conn.commit()


def db_insert_cold(conn, cursor, data):
    cursor.execute("INSERT INTO cold_water_data (value, date) VALUES (?, ?)", data)
    conn.commit()


def db_insert_elect(conn, cursor, data):
    cursor.execute("INSERT INTO electricity_data (value, date) VALUES (?, ?)", data)
    conn.commit()


def print_res(res):
    print("ID, Value, Date")
    for el in res:
        print(list(el))


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


def main():
    a = ""
    b = ""
    while a != "e" and a != "E" and a != "s" and a != "S" and a != "m" and a != "M":
        a = input("Enter, Select or select Month (E/S/M)? ")
    a = a.lower()
    if a != "m":
        while b != "h" and b != "H" and b != "c" and b != "C" and b != "e" and b != "E":
            b = input("Hot water (H), Cold water (C) or Electricity (E)? ")
        b = b.lower()

    conn, cursor = dbconn()
    # init(conn, cursor)

    if a == "e":
        value = input("Enter the data: ")
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        if b == "h":
            db_insert_hot(conn, cursor, (value, date))
        elif b == "c":
            db_insert_cold(conn, cursor, (value, date))
        else:
            db_insert_elect(conn, cursor, (value, date))
    elif a == "s":
        if b == "h":
            res = db_select_hot(conn, cursor)
        elif b == "c":
            res = db_select_cold(conn, cursor)
        else:
            res = db_select_elect(conn, cursor)
        print_res(res)
    else:
        res = db_select_hot(conn, cursor)
        if len(res) >= 2:
            val = int(res[-1][1]) - int(res[-2][1])
            print("Hot water: ", val)
        else:
            print("Not enough data for Hot Water")

        res = db_select_cold(conn, cursor)
        if len(res) >= 2:
            val = int(res[-1][1]) - int(res[-2][1])
            print("Cold water: ", val)
        else:
            print("Not enough data for Cold Water")

        res = db_select_elect(conn, cursor)
        if len(res) >= 2:
            val = int(res[-1][1]) - int(res[-2][1])
            print("Electricity: ", val)
            money = round((int(res[-1][1]) - int(res[-2][1])) * ELECTRICITY_BILL, 2)
            print("Money for Electricity: ", money)
        else:
            print("Not enough data for Electricity")

    dbclose(conn)


if __name__ == "__main__":
    main()
