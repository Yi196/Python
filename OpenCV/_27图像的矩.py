import numpy as np
import cv2


'''
矩：设x为随机变量，C为常数，则量E[(x−c)^k]称为X关于C点的k阶矩；一阶原点矩就是期望，一阶中心矩μ_1=0，二阶中心矩μ_2就是X的方差Var(X)。
在统计学上，高于4阶的矩极少使用，μ_3可以去衡量分布是否有偏，μ_4可以衡量分布（密度）在均值拘谨的陡峭程度。
空间矩的方法在图像应用中比较广泛，包括零阶矩求面积、一阶矩确定重心、二阶矩确定主方向、二阶矩和三阶矩可以推导出七个不变矩-Hu不变矩，
不变矩具有旋转，平移、缩放等不变性
'''

# 先计算轮廓
img = cv2.imread(r'./image/003.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img, contours, 2, (128, 0, 128), 5)

# 图像的矩:moments()，HuMoments()
# moments() 该函数计算多边形或栅格化形状（一个矢量形状或光栅形状）的最高达三阶所有矩
retval = cv2.moments(contours[2], False)
'''
Moments cv::moments(
InputArray array,			// 光栅图像(单通道、8位或浮点二维数组)或二维点(点或点2f)的数组(1×N或N×1)
bool binaryImage = false 	// binaryImage用来指示输出图像是否为一幅二值图像，如果是二值图像，则图像中所有非0像素看作为1进行计算。
返回值Moments类型(C++中为结构体 Python中为字典)：包含10个空间矩，7个中心矩，7个中心归一化矩
)'''
# 轮廓面积
print('轮廓面积', retval['m00'])

# 轮廓质心
point_m = [retval['m10']/retval['m00'], retval['m01']/retval['m00']]
cv2.circle(img, (int(point_m[0]), int(point_m[1])), 2, (0,0,255), -1)
print('轮廓质心', point_m)



# HuMoments()函数用于由中心矩计算Hu不变矩
hu = cv2.HuMoments(retval)   # 输入为cv2.moments()计算的中心矩
print('hu:七个不变矩-Hu不变矩:不变矩具有旋转，平移、缩放等不变性; 可用于判断图像一致性')


cv2.imshow('img', img)
cv2.waitKey(0)