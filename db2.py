import sqlite3

a = []
conn = sqlite3.connect('sample.db')
cur = conn.cursor()

sql = """SELECT x FROM main"""
cur.execute(sql)

getx = cur.fetchall()
# for x in getx:
#     a.append(x[0])
a = [x[0] for x in getx]

goukei = 0
for num in a :
    goukei += num

print(goukei)

sql = """UPDATE main SET x = ?""", [goukei]
cur.execute(sql)
