import cv2
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img= cv.imread('./image/004.jpg')

# 卷积（滤波是使用不同的卷积核进行卷积）
kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], np.float32)  # 此卷积核可强化白色像素 图像锐化
blur_1 = cv2.filter2D(img, -1, kernel)  # -1表示输出图像数据类型与输入图像一致  kernel卷积核  anchor卷积锚点（默认核中心） delta卷积结果会加上此偏移量  borderType边缘处理方式
kernel = np.ones((10,10))/100  # 均值滤波的核结构
blur_2 = cv2.filter2D(img, -1, kernel)

# 双边滤波  保边降噪
blur = cv.bilateralFilter(img, 9, 75, 75)  # 9 邻域直径，两个 75 分别是空间高斯函数标准差，灰度值相似性高斯函数标准差

# 均值滤波  会使图像变模糊
img1 = cv.blur(img, ksize=(5, 5))    # ksize为卷积核的大小 (5,5)

# 高斯滤波  用于处理高斯噪声（彩色斑点）
'''以(3,3)的邻域为例，均值滤波是对这九个数求平均，而高斯滤波是对这个九个数求加权平均，其中心思想是邻域中每个点离中心点的距离不一样，
不应该像均值滤波一样每个点的权重一样，而是离中心点越近，权值越大。而每个点的权重就是高斯分布（也就是正态分布）
opencv实现的高斯滤波，是对传入的sigmaX，sigmaY分别产生两个一维卷积核，然后分别再行和列上做卷积，其中sigmaX和sigmaY如果没有传入参数，则由ksize计算得到'''
img2 = cv.GaussianBlur(img, ksize=(3,3), sigmaX=1)   # ksize为高斯卷积核大小 注意为奇数且可不同（3，5）  sigmaX为水平方向标准差  sigmaY为垂直方向标准差 缺省是默认与X相等

# 中值滤波  对核内像素值排序取中值 可有效去除突出的亮暗点 保留边缘 用于处理椒盐噪声（黑白点）
img3 = cv.medianBlur(img, ksize=3)                # ksize=3 卷积核大小


fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,8), dpi=100)
axes[0][0].imshow(img1[:, :, ::-1])
axes[0][1].imshow(img2[:, :, ::-1])
axes[0][2].imshow(img3[:, :, ::-1])
axes[1][0].imshow(blur[:, :, ::-1])
axes[1][1].imshow(blur_1[:, :, ::-1])
axes[1][2].imshow(blur_2[:, :, ::-1])
plt.show()