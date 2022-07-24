import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('./image/001.jpg')
template = cv.imread('./image/005.jpg')  #用于匹配的模板
h,w = template.shape[:2]

#模板匹配   只能匹配相似且大小一致的图    对于尺度变化 视角变化 旋转变化 光照变化。。用关键点匹配 用SIFT和SURF算法
res = cv.matchTemplate(img,template,cv.TM_CCOEFF)  #生成一个结果矩阵  cv.TM_CCOEFF利用相关系数匹配 值越大越好 cv.TM_CCORR为’相关匹配‘值越大越好
min_val,max_val,min_loc,max_loc = cv.minMaxLoc(res)  #从结果矩阵中找出最值
top_left = max_loc  #根据不同的匹配方法选择最值
bottom_right = (top_left[0]+w,top_left[1]+h)  #由匹配模板的宽和高算出 矩形的右下角坐标
cv.rectangle(img,top_left,bottom_right,(0,255,0),8)  #在原图上框选出匹配结果

#霍夫变换 用于提取图像中的直线和圆
img2 = cv.imread('./image/006.jpg')  #读入原图 用以显示
gray_img = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)  # 转为灰度图
#霍夫线检测
#先Canny边缘检测
gauss_img = cv.GaussianBlur(gray_img,(3,3),1)
img2_1 = cv.Canny(gauss_img,50,100)
#线检测
lines = cv.HoughLines(img2_1,0.8,np.pi/180,100)  #参数为 图片 ρ精度 0精度 阈值
# HoughLinesP()概率Hough变换 是标准Hogh变换的优化版本。该函数的计算代价会少一些，执行会变得更快
lines_1 = cv.HoughLinesP(img2_1,1,np.pi/180,100, 200, 5)  # 200:最小直线长度 5:最大线段间隙
#绘制直线
for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = rho*a
    y0 = rho*b
    x1 = int(x0+1000*(-b))
    y1 = int(y0+1000*a)
    x2 = int(x0-1000*(-b))
    y2 = int(y0-1000*a)
    cv.line(img2,(x1,y1),(x2,y2),(0,255,0),5)   #显示时可显示原图


#圆检测
img3 = cv.imread('./image/007.jpg')
gray_img=cv.cvtColor(img3,cv.COLOR_BGR2GRAY)
#先中值滤波
gray_img = cv.medianBlur(gray_img,5)
#Canny边缘检测
img3_1 = cv.Canny(gray_img,50,100)
#圆检测
circles = cv.HoughCircles(img3_1,cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=20,maxRadius=50)
# cv.HOUGH_GRADIENT:检测的方法，霍夫梯度 dp=1:检测的圆与原始图像具有相同的大小，dp=2,检测的圆是原始图像的一半
# 20:检测到的相邻圆的中心的最小距离
# param1：在#HOUGHŠu梯度的情况下，它是较高的. 两个阈值传递到Canny边缘检测器（较低的一个小两倍）。
# param2：在#HOUGHŠu梯度的情况下，它是检测阶段圆心的累加器阈值。它越小，就越可能检测到假圆；
#绘制圆
for i in circles[0,:]:
    # draw the outer circle
    cv.circle(img3,(int(i[0]) , int(i[1]) ),int(i[2]),(0,255,0),2)
    # draw the center of the circle
    cv.circle(img3,(int(i[0]), int(i[1]) ),2,(0,0,255),-1)

# minEnclosingCircle() 寻找包裹轮廓的最小圆
# center, radius = cv.minEnclosingCircle(points)  # points输入的二维点集

#显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig,axes=plt.subplots(nrows=4,ncols=1,figsize=(10,8),dpi=100)
axes[0].imshow(template[:,:,::-1])
axes[0].set_title('匹配内容')
axes[1].imshow(img[:,:,::-1])
axes[1].set_title('匹配结果')
axes[2].imshow(img2[:,:,::-1])
axes[2].set_title('直线检测')
axes[3].imshow(img3[:,:,::-1])
axes[3].set_title('圆检测')
plt.show()