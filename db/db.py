from msilib.schema import tables
from optparse import Values
import sqlite3

dbname = ('main.db')
conn = sqlite3.connect(dbname, isolation_level = None)
cursor = conn.cursor()

sql = """CREATE TABLE IF NOT EXISTS road_info(cross_name_1 text, cross_name_2 text, dist float, oneway int)"""
cursor.execute(sql)
conn.commit()
sql = """CREATE TABLE IF NOT EXISTS cross_position(cross_name text, x float, y float)"""
cursor.execute(sql)
conn.commit()

sql = """INSERT INTO road_info VALUES(?, ?, ?, ?)"""
data = (('A', 'B', 10, 1))
cursor.execute(sql, data)
conn.commit()

data = (('A', 'C', 15, 1))
cursor.execute(sql, data)
conn.commit()

data = (('B', 'C', 10, 1))
cursor.execute(sql, data)
conn.commit()



