import sqlite3

dbname = ('sample.db')
conn = sqlite3.connect(dbname, isolation_level = None)

cursor = conn.cursor()

sql = """CREATE TABLE "IF NOT EXISTS main(id, x, y)"""
cursor.execute(sql)

sql = """INSERT INTO main VALUES(?, ?, ?)"""
data = [
    (1, 100, 200)
    (2, 250, 150)
]
