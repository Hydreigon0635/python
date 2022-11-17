import sqlite3
import tkinter

dbname = ('./db/simulator2.db')
conn = sqlite3.connect(dbname, isolation_level= None)
cur = conn.cursor()
cross_info = []
def timer_func():
    cur.execute(
        f"SELECT x, y FROM cross_position"
    )
    cross_info = cur.fetchall()
    for c in cross_info:
        print(c[0])
        canvas.create_oval(c[0] / 1.1 - 5, c[1] / 1.1 - 5, c[0] / 1.1 + 5, c[1] / 1.1 + 5, fill = "#000000")
        canvas.create_text(c[0] / 1.1 - 20, c[1] / 1.1 - 20, text = f"{c}")

root = tkinter.Tk()
root.title(u'Canvas Sample')
root.geometry("1200x800")
canvas = tkinter.Canvas(root, width = 800, height = 450)
canvas.place(x = 0, y = 0)
timer_func()
root.mainloop()