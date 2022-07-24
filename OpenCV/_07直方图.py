import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('./image/001.jpg', 0)
# 直方图  一般只统计灰度图
hist_img = cv.calcHist([img], [0], None, [256], [0, 256])
# 注意都要用[]传入数据 依次为 channels=[0]   指定通道 灰度图[0]  彩色图[0][1][2]>>B G R通道
#                        mask=None      掩膜图像 用于指定统计范围 None表示统计全图
#                        histSize=[256] Bin数即将直方图分组数
#                        range=[0,256]  指定统计的像素范围

# 掩膜 mask将想要统计的部分置为1 不想统计部分为零
mask = np.zeros(img.shape[0:2], np.uint8)
mask[200:700, 400:1300] = 1
# mask = cv2.bitwise_not(mask)     # 反转颜色
mask_img = cv.bitwise_and(img, img, mask=mask)  # 掩膜后的图像  注意此处要写上‘mask=’ 因为默认为None，前面还有一个参数None 不指明会传入前一个参数
mask_hist = cv.calcHist([img], [0], mask, [256], [0, 256])

# 直方图均衡化 用于曝光过度、不足 提高对比度 不推荐
equ_img = cv.equalizeHist(img)

'''*************************************************************************'''
# 自适应的直方图均衡化  提高对比度  推荐
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))   # clipLimit=2.0对比度限制 默认40 常用2.0 3.0 4.0    tileGridSize=(8,8)分块的小 默认8X8
clahe_img = clahe.apply(img)  # 注意为单通道灰度图
'''*************************************************************************'''

# 显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 8), dpi=100)
axes[0].plot(hist_img)  # 折线图
axes[0].grid()  # 加栅格
axes[0].set_title('统计全图')
axes[1].imshow(mask_img, plt.cm.gray)
axes[1].set_title('掩膜后图像')
axes[2].plot(mask_hist)  # 折线图
axes[2].grid()  # 加栅格
axes[2].set_title('统计掩膜部分')
plt.show()

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 8), dpi=100)
axes[0].imshow(img, plt.cm.gray)
axes[0].set_title('原图')
axes[1].imshow(equ_img, plt.cm.gray)
axes[1].set_title('直方图均衡化图像')
axes[2].imshow(clahe_img, plt.cm.gray)
axes[2].set_title('自适应的直方图均衡化图像')
plt.show()