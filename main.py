import sqlite3


def dbconn():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    return (conn, cursor)


def init(conn, cursor):
    cursor.execute("")


def main():
    a = ""
    while a != "e" and a != "E" and a != "s" and a != "S":
        a = input("Enter or Select (E/S)? ")

    conn, cursor = dbconn()

    init(conn, cursor)



if __name__ == "__main__":
    main()
