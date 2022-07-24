import cv2 as cv
import numpy as np


#CamShift算法 目标追踪  在MeanShift算法收敛后 根据匹配区域自动生成边框
# 设置初始化的窗口位置
x,y,w,h = 180,100,300,300 # 设置初试窗口位置和大小
track_window = (x,y,w,h)

# cap = cv.VideoCapture('./image/003.avi')
cap = cv.VideoCapture(0)

ret, frame= cap.read()

#  1  计算直方图
# 设置追踪的区域
# roi = frame[y:y+h, x:x+w]
# roi区域的hsv图像
hsv_roi = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
# 取值hsv值在(0,60,32)到(180,255,255)之间的部分
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
        ret, track_window = cv.CamShift(dst, track_window, term_crit)
        # Draw it on image
        pts = cv.boxPoints(ret)
        pts = np.int0(pts)   #np.int0就是int64的别名
        #polylines()画多个多边形  参数：图像,[多边形上点的数组],多边形是否闭合,颜色,线粗
        img2 = cv.polylines(frame,[pts],True, 255,2)
        cv.imshow('frame',img2)
    #按'ESC'键或'Q'键退出
    if cv.waitKey(25) & 0xFF == 27 or cv.waitKey(25) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()