import cv2
import numpy as np

img = cv2.imread(r'./image/007.jpg')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 获取具体HSV数值
def getpos(event, x, y, flags, param):
    if event ==cv2.EVENT_LBUTTONDOWN:    # 定义一个鼠标左键点击事件
        print(img_hsv[y, x])

cv2.imshow('img_hsv', img_hsv)
cv2.setMouseCallback('img_hsv', getpos)
cv2.waitKey(0)


# 提取红色范围
# 利用HSV色彩空间表和cv2.inRange()函数 将范围内的像素设为255 外的设为0
lower_red = np.array([0, 43, 46])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(img_hsv, lower_red, upper_red)

cv2.imshow('hsv', mask)
cv2.waitKey()

# kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
mask = cv2.bitwise_not(mask)
img = cv2.bitwise_and(img, img, mask=mask)
cv2.imshow('hsv', img)
cv2.waitKey(0)