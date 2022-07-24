import os
import cv2
import numpy as np


def get_xy(img):
    '''获取鼠标点击处的坐标值'''
    def getpos(event,x,y,flags,param):
        if event ==cv2.EVENT_LBUTTONDOWN:   #定义一个鼠标左键点击事件
            print((x,y),'  ',img[y,x])

    cv2.namedWindow('img',0)
    cv2.resizeWindow('img',1920,1080)
    cv2.imshow('img',img)
    cv2.setMouseCallback('img',getpos)
    cv2.waitKey(0)


if __name__ == '__main__':
    # img = cv2.imread(r'./image/009.jpg')
    dir = r'../../696'
    for name in os.listdir(dir):
        img = cv2.imread(os.path.join(dir,name))
        get_xy(img)