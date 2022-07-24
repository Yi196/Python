import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(r'./image/008.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# 图像分割方法
# 1、基于灰度阈值分割（调节阈值二值化提取目标区域后做为掩膜在分割出目标区域）
# 1.1直方图技术（先求图像直方图，根据直方图中不同的波峰信息，寻找目标区域）
# hist = cv2.calcHist([img_gray], [0], None, [256], [0,256])  # 计算直方图 选择合适阈值
# plt.plot(hist)
# plt.show()
_, binary = cv2.threshold(img_gray, 40, 255, cv2.THRESH_TOZERO)
_, binary = cv2.threshold(binary, 121, 255, cv2.THRESH_TOZERO_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
img_erode = cv2.erode(binary, kernel, iterations=2)

cv2.namedWindow('001', 0)
cv2.imshow('001', img_erode)
# 1.2最小误差阈值法
# 1.3最大误差阈值法
'''1、利用直方图选取初始阈值并将图像分为两组 2、计算两组像素之间方差 3、找到使方差最大的阈值'''
_, binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)
# 1.4分水岭算法
from _24分水岭算法 import watershed
# markers = watershed(img)
# cv2.imshow('markers', markers)


img_pl = cv2.imread(r'./image/poli.jpg')
# 2、基于边缘分割
# 2.1点检测（图像中孤立点对于点检测模板有较大响应）
temp_point = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])
img_point = cv2.filter2D(img_pl,0,temp_point)
cv2.imshow('img_point', img_point)
# 2.2线检测（两个轴向、45度、135度线检测模板）图像灰度恒定的区域，对这四个模板响应为0
temp_line_x = np.array([[-1,-1,-1], [2,2,2], [-1,-1,-1]])
temp_line_y = np.array([[-1,2,-1], [-1,2,-1], [-1,2,-1]])
temp_line_45 = np.array([[-1,-1,2], [-1,2,-1], [2,-1,-1]])
temp_line_135 = np.array([[2,-1,-1], [-1,2,-1], [-1,-1,2]])
img_line = cv2.filter2D(img_pl, 0, temp_line_135)
cv2.imshow('img_line', img_line)

# 去除垂直、水平直线
temp_line_h = np.array([[-1,2,-1]])
temp_line_v = np.array([[-1],[2],[-1]])
img_line = cv2.filter2D(img_line, 0, temp_line_h)
# 2.3先提取图像边缘(Soebl,Laplacian,Canny)，根据边缘分割目标区域

# 3、基于区域分割
# 3.1区域生长法（先确定种子像素，判断领域像素与种子是否有相似性）
'''确定种子像素：人机交互式分割、基于直方图的粗分割结果作为种子
确定相似性：基于区域灰度差、基于区域灰度分布统计性质'''
from _25生长算法 import regionGrow
# img_grow = regionGrow(img, [[1, 1]], 10)

# 3.2分裂合并法（将图像分为任意大小且不重叠的区域，再合并或分裂这些区域（基于灰度统计特征））
from _26区域分裂合并算法 import regionSpilt
# img_split = regionSpilt(img, 10, 10, 150)

# 4、基于学习的分割 K-Means聚类 FCN MASK-RCNN



cv2.waitKey(0)