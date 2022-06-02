import numpy as np
import time

#ユークリッド計算法とマンハッタン計算法の処理速度の比較
if __name__ == '__main__':
    start = time.time()
    for i in range(0, 10000):
        x = np.array([1, 1])
        y = np.array([2, 2])
        np.linalg.norm(x - y, ord = 1)
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

#マンハッタンのほうがびみょーに早い（内容による）