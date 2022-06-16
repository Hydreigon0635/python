import sqlite3

dbname = ('sample.db')
conn = sqlite3.connect(dbname, isolation_level = None)

cursor = conn.cursor()

sql = """CREATE TABLE IF NOT EXISTS main(id, x, y)"""
cursor.execute(sql)
conn.commit()

cursor.execute('DELETE FROM main')
conn.commit()

sql = """INSERT INTO main VALUES(?, ?, ?)"""
data = ((1, 100, 200))
cursor.execute(sql, data)
conn.commit()

data = ((2, 150, 250))
cursor.execute(sql, data)
conn.commit()

data = ((3, 200, 300))
cursor.execute(sql, data)
conn.commit()

data = ((4, 250, 350))
cursor.execute(sql, data)
conn.commit()
