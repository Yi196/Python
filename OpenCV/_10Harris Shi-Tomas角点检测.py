import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('./image/003.jpg')
img2 = img.copy()
img3 = img.copy()
gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = gray_img.copy()
gray_1 = gray_img.copy()


#Harris算法 角点检测 有旋转不变性  没有尺度不变性 不推荐
gray_img = np.float32(gray_img)           #输入图像要为float32   或 gray_img.astype(np.float32)
dst = cv.cornerHarris(gray_img,2,3,0.04)    #参数为 灰度图 领域大小2 Sobel求导时的卷积核大小3 角点检测中的自由参数0.04-0.06
#设置阈值 绘制角点
img[dst > 0.001*dst.max()] = [0,0,255]


#Shi-Tomas算法 角点检测 有旋转不变性  没有尺度不变性  推荐
corners = cv.goodFeaturesToTrack(gray_1,1000,0.05,10)  #参数为 灰度图 最大角点数目 最低角点质量0-1 角点间最小距离
#绘制角点
for i in corners:
    x,y = i.ravel()
    cv.circle(img2,( int(x) ,int(y) ),2,(0,0,255),-1)


#cornerSubPix亚像素级角点检测
_, binary = cv.threshold(gray,50,255,cv.THRESH_BINARY)
contours, hireachy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)    #注意此处只能传入单通道二值化图像
cont = list(contours)[0].astype(np.float32)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.1)     #用于表示计算亚像素时停止迭代的标准
corners = cv.cornerSubPix(gray, cont, (5,5), (-1,-1), criteria)     #第三个参数是计算亚像素角点时考虑的区域的大小  第四个忽略
#绘制角点
for i in corners:
    x,y = i.ravel()
    cv.circle(img3,( int(x) ,int(y) ),2,(0,0,255),-1)


#显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig,axes=plt.subplots(nrows=1,ncols=3,figsize=(10,8),dpi=100)
axes[0].imshow(img[:,:,::-1])
axes[0].set_title('Harris算法 角点检测')
axes[1].imshow(img2[:,:,::-1])
axes[1].set_title('Shi-Tomas算法 角点检测')
axes[2].imshow(img3[:,:,::-1])
axes[2].set_title('SubPix算法 角点检测')
plt.show()