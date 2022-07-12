from cmath import sqrt
import sqlite3

def a_star(start:str, goal:str, disable:list):
    conn = sqlite3.connect(dbname, isolation_level=None)
    cur = conn.cursor()
    now_node = start
    passed_node_list = []
    node_info = {start:[0, 0]} #辞書型（交差点名：[それまでの距離合計, コスト]）
    #コスト　＝　実際の距離　＋　ゴールとの直線距離
       
    while True:
        #now_nodeから移動可能なcross_nameを抽出する
        connect_node_info = []
        sql = f"SELECT * FROM road_info(WHERE node2 == '{now_node}' AND oneway != 1)"
        cur.execute(sql)
        can_move_node_tmp = cur.fetchall()
        connect_node_info = [(c[0], c[2], c[3]) for c in can_move_node_tmp]
        
        sql = f"SELECT * FROM road_info(WHERE node1 == '{now_node}' AND oneway != 2)"
        cur.execute(sql)
        can_move_node_tmp = cur.fetchall()
        connect_node_info += [(c[1], c[2], c[3]) for c in can_move_node_tmp] 
        # cn : 探索中ノードの情報（交差点名, 距離, 一方通行）
        for cn in connect_node_info:
            if not cn[0] in disable:
                dist1 = node_info[now_node][0] + cn[1]
                dist2 = euclid(cn[0] , goal)
                cost = dist1 + dist2
                if not cn in node_info:
                    # node_info[cn[0]] = 1 # TODO 現在のコスト
                    node_info[cn[0]][0] = dist1
                    node_info[cn[0]][1] = cost

                elif node_info[cn[0]][1] > cost:
                    node_info[cn] = cost

        disable.append(now_node)
        passed_node_list.append(now_node)
        #now_node更新処理
        min = float('inf')
        for key in node_info:
            if (node_info[key][1] < min) and (not key in disable):
                min = node_info[key][1]
                now_node = key   
        
        if now_node == goal:
            return passed_node_list

        

                 


def euclid(cross_name, goal_name):
    node_info = []
    conn = sqlite3.connect(dbname, isolation_level=None)
    cur = conn.cursor()
    sql = f"SELECT * FROM cross_position WHERE cross_name = '{cross_name}' OR cross_name = '{goal_name}')"
    cur.execute(sql)
    now_node_info = cur.fetchall()


    dist_x = abs(node_info[0][1] - node_info[1][1])**2
    dist_y = abs(node_info[0][2] - node_info[1][2])**2 
    dist = sqrt(dist_x + dist_y)

    return dist