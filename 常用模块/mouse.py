import pyautogui as pg
import time
import sys
from threading import Thread

class Mouse():
    def __init__(self,n):
        self.mouse_x = None
        while True:
            self.x,self.y = pg.position()
            Thread(target=self._wite_n_s, args=(n,self.x,self.y)).start()
            time.sleep(0.5)
            if self.mouse_x:
                break
        print(self.mouse_x,self.mouse_y)

    #判断n秒内鼠标是否移动
    def _wite_n_s(self,n,x,y):
        if n>0:
            if x == self.x and y == self.y :
                time.sleep(0.5)
                return self._wite_n_s(n-0.5,x,y)
            else:
                return False
        else:
            self.mouse_x = x
            self.mouse_y = y
            return True



#获取鼠标悬停n秒后的值
def mouse(n):
    pos_lst = []
    while True:
        x,y = pg.position()
        pos_lst.append((x,y))
        pos_lst = pos_lst[-(2*n):]
        time.sleep(0.5)
        if pos_lst == [(x,y),] * (2*n):
            break
    print(x,y)
    return x,y


if __name__ == '__main__':
    #法一：定义类 每0.5秒开启一个线程 每个线程判断当前鼠标位置是否与启动线程时相等 满足时间后返回鼠标值
    # Mouse(3)

    #法二：每0.5秒往列表中存入当前鼠标值 并判断列表后2n位是否相同
    mouse(3)
