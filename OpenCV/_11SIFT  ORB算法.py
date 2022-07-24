import copy
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img_sift = cv.imread('./image/003.jpg')
img_surf = copy.copy(img_sift)
img_fast = copy.copy(img_sift)
img_orb = copy.copy(img_sift)
gray_img = cv.cvtColor(img_sift,cv.COLOR_BGR2GRAY)

#Opencv3.4之后SIFT SURF算法受到专利保护,20年3月后SIFT专利过期，更新cv版本即可免费使用

#SIFT算法 关键点检测  具有尺度不变性 旋转不变性
#实例化sift对象
sift = cv.SIFT_create()
#检测关键点并计算
kp = sift.detect(gray_img,None)
# kp,des = sift.detectAndCompute(gray_img,None)  #返回值 kp关键点的（位置、尺度、方向）信息   des关键点描述
#绘制结果
cv.drawKeypoints(img_sift,kp,img_sift,flags=cv.DRAW_MATCHES_FLAGS_DEFAULT)
                  #参数为原图 kp关键点信息 输出图片  flags= 显示方式 cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS为绘制带大小和方向的关键点圆


# #SIFT算法 关键点检测  具有尺度不变性 旋转不变性
# #实例化sift对象
# sift = cv.xfeatures2d.SIFT_create()
# #检测关键点并计算
# kp,des = sift.detectAndCompute(gray_img,None)  #返回值 kp关键点的（位置、尺度、方向）信息   des关键点描述
# #绘制结果
# cv.drawKeypoints(img_sift,kp,img_sift,flags=cv.DRAW_MATCHES_FLAGS_DEFAULT)
#             #参数为原图 kp关键点信息 输出图片  flags= 显示方式 cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS为绘制带大小和方向的关键点圆此处为绘制带大小和方向的关键点圆


# #SURF算法（性能优于SIFT算法） 具有尺度不变性 旋转不变性
# surf = cv.xfeatures2d.SURF_create()
# #检测关键点并计算
# kp,des = surf.detectAndCompute(gray_img,None)
# #绘制结果
# cv.drawKeypoints(img_surf,kp,img_surf,flags=cv.DRAW_MATCHES_FLAGS_DEFAULT)


#FAST算法 角点检测 无不变性
fast = cv.FastFeatureDetector_create(threshold=30)  #前两个参数为 阈值默认10  是否开启极大值抑制True
kp = fast.detect(gray_img,None)  #此处可传入彩图
cv.drawKeypoints(img_fast,kp,img_fast,(0,0,255))

#ORB算法  关键点检测  具有尺度不变性 旋转不变性 （无专利保护）
orb = cv.ORB_create(400)  #参数为 特征点的最大数量 可缺省
kp,des = orb.detectAndCompute(gray_img,None) #计算图像中的特征点和描述符
cv.drawKeypoints(img_orb,kp,img_orb,(0,0,255),flags=0)


#显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig,axes=plt.subplots(nrows=4,ncols=1,figsize=(10,8),dpi=100)
axes[0].imshow(img_sift[:,:,::-1])
axes[0].set_title('SIFT算法 关键点检测')
axes[1].imshow(img_surf[:,:,::-1])
axes[1].set_title('SURF算法 关键点检测')
axes[2].imshow(img_fast[:,:,::-1])
axes[2].set_title('FAST算法 角点检测')
axes[3].imshow(img_orb[:,:,::-1])
axes[3].set_title('ORB算法 关键点检测')
plt.show()