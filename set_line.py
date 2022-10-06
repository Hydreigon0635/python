import tkinter
import sqlite3

dbname = "./db/sub.db"
conn = sqlite3.connect(dbname, isolation_level = None)
cur = conn.cursor()

def set_line():
    print("aaa")
    cur.execute(
        f"SELECT cross_name_1, cross_name_2, oneway FROM road_info")
    cross_info = cur.fetchall()
    for c in cross_info:
        cur.execute(
            f"SELECT x, y FROM cross_position WHERE cross_name == '{c[0]}'")
        cross_position_1 = cur.fetchone()
        canvas.create_oval(cross_position_1[0] * 5 - 5, cross_position_1[1] * 5 - 5, cross_position_1[0] * 5 + 5, cross_position_1[1] * 5 + 5, fill = "#000000")
        cur.execute(
            f"SELECT x, y FROM cross_position WHERE cross_name == '{c[1]}'") 
        cross_position_2 = cur.fetchone()
        canvas.create_oval(cross_position_2[0] * 5 - 5, cross_position_2[1] * 5 - 5, cross_position_2[0] * 5 + 5, cross_position_2[1] * 5 + 5, fill = "#000000")
        if c[2] == 0:
            canvas.create_line(cross_position_1[0] * 5, cross_position_1[1] * 5, cross_position_2[0] * 5, cross_position_2[1] * 5, tag = 'line', arrow = tkinter.FIRST)
        elif c[2] == 1:
            canvas.create_line(cross_position_1[0] * 5, cross_position_1[1] * 5, cross_position_2[0] * 5, cross_position_2[1] * 5, tag = 'line', arrow = tkinter.LAST)
        elif c[2] == 2:
            canvas.create_line(cross_position_1[0] * 5, cross_position_1[1] * 5, cross_position_2[0] * 5, cross_position_2[1] * 5, tag = 'line', arrow = tkinter.FIRST)

root = tkinter.Tk()
root.title(u'Canvas Sample')
root.geometry("800x450")
canvas = tkinter.Canvas(root, width = 800, height = 450)
canvas.place(x = 0, y = 0)
set_line()
root.mainloop()