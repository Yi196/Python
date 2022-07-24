import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('image/001.jpg')
# 通道拆分
b,g,r= cv.split(img)
plt.imshow(b,plt.cm.gray)    # 以灰度图  将b通道显示
plt.show()
# 通道合并
img2=cv.merge((b,g,r))
plt.imshow(img2[:,:,::-1])
plt.show()

# 色彩空间转换  BGR》GRAY  BGR》HSV
# BGR》GRAY
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
plt.imshow(gray,plt.cm.gray)
plt.show()
# BGR》HSV MeanShift算法 CamShift算法 目标追踪 效果更好
hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)
plt.imshow(hsv)
plt.show()

'''
THRESH_BINARY；二值化阈值处理：灰度值大于阈值的点，将其灰度值设定为最大值，灰度值小于或等于阈值的点，将其灰度值设定为0
THRESH_BINARY_INV；反二值化阈值处理：灰度值大于阈值的点，将其灰度值设定为0，灰度值小于或等于阈值的点，将其灰度值设定为最大值
THRESH_TRUNC；截断阈值化处理：灰度值大于阈值的点，将其灰度值设定为阈值，灰度值小于或等于阈值的点，其灰度值保持不变
THRESH_TOZERO；低阈值零处理：灰度值大于阈值的点，其灰度值保持不变，灰度值小于或等于阈值的点，将其灰度值设定为0
THRESH_TOZERO_INV；高阈值零处理：灰度值大于阈值的点，将其灰度值设定为0，灰度值小于或等于阈值的点，其灰度值保持不变
'''
# 图像二值化
retval1, dst1 = cv.threshold(gray, 40, 255, cv.THRESH_BINARY)
# retval1阈值 dst返回的二值图像  灰度图 40阈值 255最大值  方法（此处为 大于阈值40置为最大值255） cv.THRESH_BINARY_INV 与其相反大于阈值置为0

# cv.THRESH_OTSU 会忽略阈值 自动计算一个合适的全局阈值
'''1、利用直方图选取初始阈值并将图像分为两组 2、计算两组像素之间方差 3、找到使方差最大的阈值'''
retval2, dst2 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

# 自适应二值化，为不同区域计算不同的阈值  对于去除背景，提取前景效果较好
binary_ada = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize=33, C=20) # blockSize越大单个区域越大 细节轮廓越少整体轮廓越粗越明显  C越大整体图像白色像素越多
# 输入图像 满足条件点设置为2255 自适应方法cv.ADAPTIVE_THRESH_MEAN_C  二值化方法 blockSize:分割计算的区域大小取奇数  C:常数 每个区域计算出的阈值再减去C为最终阈值 可为负
binary_ada_1 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize=55, C=10)


# 通过cv2.applyColorMap()函数，我们可以将灰度图转换成红色-蓝色的热力图，当值为255时，为红色，当值为0时，为蓝色
img_gray = cv.imread(r'./image/006.jpg',0)
heat_img = cv.applyColorMap(img_gray, cv.COLORMAP_JET)
cv.imshow('',heat_img)
cv.waitKey()


# 显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8,10), dpi=100)
axes[0][0].imshow(dst1, plt.cm.gray)
axes[0][0].set_title('二值化 指定阈值')
axes[0][1].imshow(dst2, plt.cm.gray)
axes[0][1].set_title('二值化 自动生成阈值')
axes[1][0].imshow(binary_ada, plt.cm.gray)
axes[1][0].set_title('自适应二值化 分区域生成不同阈值')
axes[1][1].imshow(binary_ada_1, plt.cm.gray)
axes[1][1].set_title('自适应二值化 分区域生成不同阈值')
plt.show()


# 图像加法
img3 = cv.add(img, img2)  #超过255 为255
# 图像混合
img4 = cv.addWeighted(img, 0.3, img2, 0.7, 0)    #混合后再加一个常量 此处为0
