import cv2 as cv
import numpy as np


#MeanShift算法 目标追踪  窗口大小不变
# 设置初始化的窗口位置
r,h,c,w = 330,280,800,280 # 设置初试窗口位置和大小
track_window = (c,r,w,h)
#载入图像
cap = cv.VideoCapture('./image/003.avi')

#先读取一帧 用于指定初始的追踪区域
ret, frame= cap.read()

#  1  计算直方图
# 设置追踪的区域
roi = frame[r:r+h, c:c+w]
# roi区域的hsv图像
hsv_roi = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
# 取值hsv值在(0,60,32)到(180,255,255)之间的部分  去除低亮度的值
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
# 计算直方图,参数为 图片(可多)，通道数，蒙板区域，直方图长度，范围
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
# 归一化
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)


#  2  目标追踪
# 设置终止条件，迭代10次或者至少移动1次
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

while True:
    ret, frame = cap.read()
    if ret == True:
        # 计算每一帧的hsv图像
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # 计算反向投影
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # 调用meanShift算法在dst中寻找目标窗口，找到后返回目标窗口
        ret, track_window = cv.meanShift(dst, track_window, term_crit)
        # Draw it on image
        x,y,w,h = track_window
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv.imshow('frame',img2)
        cv.resizeWindow('frame', 1920, 1080)

    if cv.waitKey(25) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
