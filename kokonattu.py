from re import X
import sys
import tkinter
import random

point = {"x":0,"y":0}

def timer_func():
    global point
    print(point)
    tmp = {"x":0, "y":0}
    tmp["x"] = random.uniform(0, 450) 
    tmp["y"] = random.uniform(0, 450)
    canvas.create_oval( point["x"]- 5, point["y"]-5, point["x"] + 5, point["y"] + 5, tag = "oval")
    print("円の中心", point["x"], point["y"])
    canvas.create_line(point["x"], point["y"], tmp["x"], tmp["y"])
    point = tmp
    root.after(100, timer_func)

root = tkinter.Tk()
root.title(u'Canvas Sample')
root.geometry("800x450")
canvas = tkinter.Canvas(root, width = 800, height = 450)
canvas.place(x = 0, y = 0)
timer_func()
root.mainloop()