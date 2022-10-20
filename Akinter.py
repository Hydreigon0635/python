from cgitb import text
import tkinter
import sqlite3
import cmath
import time


def create_oval(x_1, y_1, x_2, y_2, color: text):
    canvas.create_oval(x_1 * 5 - 5, y_1 * 5 - 5, x_2 *
                       5 + 5, y_2 * 5 + 5, fill=color)


def set_line():
    print('aaa')
    cur.execute(
        f"SELECT cross_name_1, cross_name_2, oneway FROM road_info")
    cross_info = cur.fetchall()
    print(cross_info)

    for c in cross_info:
        cur.execute(
            f"SELECT x, y FROM cross_position WHERE cross_name == '{c[0]}'")
        cross_position_1 = cur.fetchone()
        create_oval(cross_position_1[0], cross_position_1[1],
                    cross_position_1[0], cross_position_1[1], "#000000")
        cur.execute(
            f"SELECT x, y FROM cross_position WHERE cross_name == '{c[1]}'")
        cross_position_2 = cur.fetchone()
        create_oval(cross_position_1[0], cross_position_1[1],
                    cross_position_2[0], cross_position_2[1], "#000000")
        if c[2] == 0:
            canvas.create_line(cross_position_1[0] * 5, cross_position_1[1] * 5, cross_position_2[0]
                               * 5, cross_position_2[1] * 5, tag='line', arrow=tkinter.FIRST)
        elif c[2] == 1:
            canvas.create_line(cross_position_1[0] * 5, cross_position_1[1] * 5,
                               cross_position_2[0] * 5, cross_position_2[1] * 5, tag='line', arrow=tkinter.LAST)
        elif c[2] == 2:
            canvas.create_line(cross_position_1[0] * 5, cross_position_1[1] * 5, cross_position_2[0]
                               * 5, cross_position_2[1] * 5, tag='line', arrow=tkinter.FIRST)


def euclid(cross_name, goal_name):
    cur.execute(
        f"SELECT * FROM cross_position WHERE cross_name = '{cross_name}' OR cross_name = '{goal_name}'")
    node_info = cur.fetchall()

    if len(node_info) == 1:
        return 0

    dist_x = (node_info[0][1] - node_info[1][1]) ** 2
    dist_y = (node_info[0][2] - node_info[1][2]) ** 2
    dist = abs(cmath.sqrt(dist_x + dist_y))

    return round(dist, 2)


def between(tag_id, isStart):
    cur.execute(
        f"SELECT cross_name_1,cross_name_2 FROM road_tag_info WHERE tag_id = '{tag_id}' ")
    between_cross = cur.fetchone()

    cross_name = ""
    if between_cross:
        if isStart:
            cross_name = between_cross[0]
        else:
            cross_name = between_cross[1]
    else:
        cross_name = tag_id
    return cross_name


def a_star():
    global disable_nodes
    global now_node
    global node_info
    global route_info
    global goal_cross

    cur.execute(
        f"SELECT * FROM road_info WHERE cross_name_2 = '{now_node}' AND oneway != 1")
    connect_node_info = [(c[0], c[2]) for c in cur.fetchall()]

    cur.execute(
        f"SELECT * FROM road_info WHERE cross_name_1 = '{now_node}' AND oneway != 2")
    connect_node_info += [(c[1], c[2]) for c in cur.fetchall()]
    # now_nodeから移動可能なタグをconnect_node_infoとして格納

    # 接続しているノードnode_info計算
    have_connect_node = False
    for cn in connect_node_info:
        if cn[0] in disable_nodes:
            continue

        # cost = 実際の距離 + ゴールとの直線距離
        dist = node_info[now_node][0] + cn[1]
        cost = euclid(cn[0], goal_cross) + dist
        have_connect_node = True

        if not cn[0] in node_info or node_info[cn[0]][1] > cost:
            node_info[cn[0]] = [None, None]
            node_info[cn[0]][0] = dist
            node_info[cn[0]][1] = cost

            route_info[cn[0]] = [r for r in route_info[now_node]]
            route_info[cn[0]].append(cn[0])

    if not have_connect_node:
        # 経路が見つからなかった場合
        return (False, None)

    disable_nodes.append(now_node)
    node_info.pop(now_node)
    route_info.pop(now_node)

    # 次の now_node の適任を探す
    min = float('inf')

    for key in node_info:
        if (node_info[key][1] < min) and (not key in disable_nodes):
            min = node_info[key][1]
            now_node = key

    if now_node == goal_cross:
        # 経路が見つかった場合
        return (True, route_info[goal_cross])

    # 経路探索中
    return (False, None)


def init(start_tag, goal_tag, *disable_nodes: tuple):
    global now_node
    global node_info
    global route_info
    global start_cross
    global goal_cross

    # set_line()
    start_cross = between(start_tag, True)
    goal_cross = between(goal_tag, False)

    now_node = start_cross    # 探索中のノード
    node_info = {start_cross: [0, 0]}  # 各ノードの実際の距離とコスト
    route_info = {start_cross: [start_cross]}  # あるノードまでの最短経路

    if start_cross and goal_cross:
        return True
    else:
        return False


def timer_func():
    res = a_star()
    print(res)
    if not res[0]:
        root.after(3, timer_func)


if __name__ == '__main__':
    dbname = "./db/sub.db"
    conn = sqlite3.connect(dbname, isolation_level=None)
    cur = conn.cursor()

    root = tkinter.Tk()
    root.title(u'Canvas Sample')
    root.geometry("800x450")
    canvas = tkinter.Canvas(root, width=800, height=450)
    canvas.place(x=0, y=0)

    # a_star から取り出した
    disable_nodes = []
    now_node = None    # 探索中のノード
    node_info = None  # 各ノードの実際の距離とコスト
    route_info = None  # あるノードまでの最短経路

    if init("cross_002", "cross_006"):
        timer_func()

    root.mainloop()
