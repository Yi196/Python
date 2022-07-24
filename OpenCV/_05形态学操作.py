import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('image/003.jpg')
img_1 = cv.imread('image/004.jpg')

'''应用：边界提取（原图 - 腐蚀图）、识别物体形状（击中击不中变换）、
可用与目标相同的核进行腐蚀已达到匹配目标的效果，如在含有1X1,3X3,5X5的二值图中查找5X5的矩形位置，可先用5X5的核去腐蚀图像，再用5X5的核膨胀即可'''

# 腐蚀
kernel= np.ones((5,5),np.uint8)  # 设置核结构
kernel_1 = np.ones((1,3),np.uint8)  # (1,3)可保留X方向边
kernel_2 = np.ones((3,1),np.uint8)  # (3,1)可保留Y方向边
element = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))  # 设置核结构 anchor核中心
img1= cv.erode(img,kernel,iterations=2)   # iterations为迭代次数 默认为1
# 膨胀
img2= cv.dilate(img,kernel)

# 开运算 先腐蚀后膨胀 用于消除小的干扰快 降噪
kernel = np.ones((4,4),np.uint8) # 设置核结构
img_11 = cv.morphologyEx(img_1,cv.MORPH_OPEN,kernel)
# 闭运算 先膨胀后腐蚀 用于消除闭合物体内的孔洞
img_12 = cv.morphologyEx(img_1,cv.MORPH_CLOSE,kernel)
# 礼帽运算 原图与开运算的差  分离’亮点‘
img_13 = cv.morphologyEx(img_1,cv.MORPH_TOPHAT,kernel)
# 黑帽运算 闭运算与原图的差  分离’暗点‘
img_14 = cv.morphologyEx(img_1,cv.MORPH_BLACKHAT,kernel)


# 显示
fig,axes=plt.subplots(nrows=3,ncols=3,figsize=(10,8),dpi=100)
axes[0,0].imshow(img[:, :, ::-1])
axes[0,0].set_title('Original')
axes[0,1].imshow(img1[:, :, ::-1])
axes[0,1].set_title('Erosion')
axes[0,2].imshow(img2[:, :, ::-1])
axes[0,2].set_title('Dilate')
axes[1,0].imshow(img_1[:, :, ::-1])
axes[1,0].set_title('Original')
axes[1,1].imshow(img_11[:, :, ::-1])
axes[1,1].set_title('Open')
axes[1,2].imshow(img_12[:, :, ::-1])
axes[1,2].set_title('Close')
axes[2,0].imshow(img_1[:, :, ::-1])
axes[2,0].set_title('Original')
axes[2,1].imshow(img_13[:, :, ::-1])
axes[2,1].set_title('Tophat')
axes[2,2].imshow(img_14[:, :, ::-1])
axes[2,2].set_title('Blackhat')
plt.show()