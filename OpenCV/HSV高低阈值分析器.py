# -*- coding:utf-8 -*-

import cv2
import numpy as np

# HSV高低阈值分析器
def hsv_threshold_analysis(img, lst_low=[35, 43, 35], lst_high=[90, 255, 255]):
    """
    功能：读取一张图片，显示出来，转化为HSV色彩空间
         并通过滑块调节HSV阈值，实时显示
    """

    hsv_low = np.array(lst_low)
    hsv_high = np.array(lst_high)

    # 下面几个函数，写得有点冗余

    def h_low(value):
        hsv_low[0] = value

    def h_high(value):
        hsv_high[0] = value

    def s_low(value):
        hsv_low[1] = value

    def s_high(value):
        hsv_high[1] = value

    def v_low(value):
        hsv_low[2] = value

    def v_high(value):
        hsv_high[2] = value

    cv2.namedWindow('image')
    cv2.resizeWindow('image', 600, 350)
    cv2.namedWindow('BGR', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('BGR', 600, 380)
    cv2.namedWindow('dst', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('dst', 600, 380)
    cv2.namedWindow('ret', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('dst', 600, 380)
    cv2.imshow("BGR", img)
    # 可以自己设定初始值，最大值255不需要调节
    cv2.createTrackbar('H low', 'image', lst_low[0], 255, h_low)
    cv2.createTrackbar('H high', 'image', lst_high[0], 255, h_high)
    cv2.createTrackbar('S low', 'image', lst_low[1], 255, s_low)
    cv2.createTrackbar('S high', 'image', lst_high[1], 255, s_high)
    cv2.createTrackbar('V low', 'image', lst_low[2], 255, v_low)
    cv2.createTrackbar('V high', 'image', lst_high[2], 255, v_high)

    while True:
        dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # BGR转HSV
        dst = cv2.inRange(dst, hsv_low, hsv_high) # 通过HSV的高低阈值，提取图像部分区域
        cv2.imshow('dst', dst)
        ret = cv2.addWeighted(dst,0.5,img[:,:,0],0.5,0)
        cv2.imshow('ret', ret)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()

    return hsv_low,hsv_high



# 图像HSV值调节器
def hsv_threshold_change(img):
    # 回调函数，未使用
    def nothing(x):
        pass

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 显示原图像做对比
    cv2.namedWindow('old', cv2.WINDOW_NORMAL)
    cv2.imshow('old', img)

    # 新图像窗口
    cv2.namedWindow('new', cv2.WINDOW_AUTOSIZE)
    # 初始化滚动条
    cv2.createTrackbar("H", 'new', 100, 150, nothing)
    cv2.createTrackbar("S", 'new', 100, 150, nothing)
    cv2.createTrackbar("V", 'new', 100, 150, nothing)

    while True:
        # ESC按下退出
        if cv2.waitKey(10) == 27:
            print("finish adjust picture and quit")
            break

        # 读取滚动条现在的滚动条的HSV信息
        h_value = float(cv2.getTrackbarPos("H", 'new') / 100)
        s_value = float(cv2.getTrackbarPos("S", 'new') / 100)
        v_value = float(cv2.getTrackbarPos("V", 'new') / 100)
        # 拆分、读入新数据后，重新合成调整后的图片
        H, S, V = cv2.split(img_hsv)
        new_img = cv2.merge([np.uint8(H * h_value), np.uint8(S * s_value), np.uint8(V * v_value)])
        cv2.imshow('new', new_img)

    cv2.destroyAllWindows()
    return new_img

if __name__ == '__main__':
    img = cv2.imread(r'./image/007.jpg')
    img = cv2.imread(r'../../300/001.png')
    lst_low = [0, 0, 30]
    lst_high = [83, 255, 255]

    hsv_low,hsv_high = hsv_threshold_analysis(img, lst_low, lst_high)
    print(hsv_low, hsv_high)

    # img_new = hsv_threshold_change(img)