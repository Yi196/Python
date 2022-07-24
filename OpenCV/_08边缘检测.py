import cv2,math
import numpy as np
import matplotlib.pyplot as plt

img= cv2.imread('./image/001.jpg',0)
img_1 = cv2.imread('./image/003.jpg')
img_2 = img_1.copy()
img_3 = img_1.copy()
gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)

# Sobel算子  （一阶导数最大值为边缘）对噪声敏感度较低，可以检测边缘方向，无法进行边缘定位（判断像素点在边缘内外测）
'''黑色到白色的过渡被视为正斜率（具有正值），而白色到黑色的过渡被视为负斜率（具有负值）。
输出设置为CV_8U会丢失负值。如果要检测两个边缘，更好的选择是将输出数据类型保留为更高的形式，
例如CV_16S，CV_64F等，取其绝对值，然后转换回CV_8U。'''
x = cv2.Sobel(img, cv2.CV_16S, 1, 0)    # cv.CV_16S用于转换数字类型 避免结果溢出  1，0 为求导方向
y = cv2.Sobel(img, cv2.CV_16S, 0, 1)    # 再加一个 ksize=-1 则变为Scharr算子（保留更多细节）
scale_absX = cv2.convertScaleAbs(x)   # 取绝对值 将数据转换为 np.uint8
scale_absY = cv2.convertScaleAbs(y)
result = cv2.addWeighted(scale_absX, 0.5, scale_absY, 0.5, 0)

# Scharr算子（比Sobel保留更多细节）
x = cv2.Sobel(img, cv2.CV_16S, 1, 0, ksize=-1)    # cv.CV_16S用于转换数字类型 避免结果溢出  1，0 为求导方向 x方向
y = cv2.Sobel(img, cv2.CV_16S, 0, 1, ksize=-1)
scale_absX = cv2.convertScaleAbs(x)
scale_absY = cv2.convertScaleAbs(y)
result2 = cv2.addWeighted(scale_absX, 0.5, scale_absY, 0.5, 0)  # 注意最后加个常数

# Laplacian算子 （二阶导数为零处为边缘）对噪声敏感(一般先高斯滤波)，不能检测边缘的方向，零交叉性质进行边缘定位
img_blur = cv2.GaussianBlur(img, (3,3), 1)
laplac = cv2.Laplacian(img_blur, cv2.CV_16S)  # cv.CV_16S用于转换数字类型 避免结果溢出
result3 = cv2.convertScaleAbs(laplac)      # 数据转换为 np.uint8

# 让一幅图像与它的Sobel\Laplacian算子相加 可以锐化图像
ret_4 = cv2.addWeighted(img, 1, result3, 1, 0)

'''*************************************************************************'''
# Canny边缘检测 二阶导为零   推荐
'''基于Canny算子的边缘检测主要有5个步骤，依次是高斯滤波、像素梯度计算、非极大值抑制、滞后阈值处理和孤立弱边缘抑制
Canny(img,threshold1,threshold1) threshold1、2用于滞后阈值处理：定义一个高阈值和一个低阈值。梯度强度低于低阈值的像素点被抑制，不作为边缘点；
高于高阈值的像素点被定义为强边缘，保留为边缘点；处于高低阈值之间的定义为弱边缘，留待进一步处理。
孤立弱边缘抑制：通常而言，由真实边缘引起的弱边缘像素点将连接到强边缘像素点，而噪声响应则未连接。通过查看弱边缘像素及其8个邻域像素，
可根据其与强边缘的连接情况来进行判断。一般，可定义只要其中邻域像素其中一个为强边缘像素点，则该弱边缘就可以保留为强边缘，即真实边缘点。
'''
# 先高斯滤波
gauss_img = cv2.GaussianBlur(img, (3,3), 1)
# 再检测
result4 = cv2.Canny(gauss_img, 0, 100)  # 0,100 梯度强度低于低阈值的像素点被抑制，不作为边缘点 高于高阈值的像素点被定义为强边缘
'''*************************************************************************'''

# 轮廓检测cv2.findContours()函数接受的参数为二值图
_, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)  # 图像二值化
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 轮廓检测  cv.CHAIN_APPROX_SIMPLE取直线
# cv.drawContours(img_1, contours, -1, (128, 0, 128), 5) #画出轮廓  #contourdx= -1 表示画出所有轮廓
'''第一个参数是寻找轮廓的图像(二值图)；
第二个参数表示轮廓的检索模式，有四种（本文介绍的都是新的cv2接口）：
    cv2.RETR_EXTERNAL表示只检测外轮廓
    cv2.RETR_LIST检测的轮廓不建立等级关系
    cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
    cv2.RETR_TREE建立一个等级树结构的轮廓。
第三个参数method为轮廓的近似办法
    cv2.CHAIN_APPROX_NONE存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
    cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
'''
# 计算轮廓周长
length = cv2.arcLength(contours[0], closed=True)  # closed=True 轮廓是否闭合

# 将轮廓按面积降序排序
def cont_area(cont):
    return cv2.contourArea(cont)
list(contours).sort(key=cont_area,reverse=True)
cv2.drawContours(img_1, contours, 0, (128, 0, 128), 5)  # 画出面积最大的轮廓

# 按轮廓抠图
cimg = np.zeros_like(img_2)
cv2.drawContours(cimg, contours, 0, color=(1, 1, 1), thickness=-1)
img_final = img_2 * cimg  # 非选定区域为黑色
# cimg[:, :, :] = 255       # 非选定区域为白色
# cv2.drawContours(cimg, contours, 0, color=(0, 0, 0), thickness=-1)  # thickness=-1 表示将轮廓区域全部填充
# img_final = cv2.bitwise_or(img_2, cimg)


# 画出面积最大的轮廓
# a = np.array(list(map(cv.contourArea,contours))).argmax()
# cv.drawContours(img_1, contours, a, (128, 0, 128), 5)

# 找外接矩形(矩形水平放置)
x, y, w, h = cv2.boundingRect(contours[1])
cv2.rectangle(img_1, (int(x), int(y)), (int(x+w), int(y+h)), (128,128,0), 5)
# bounding_boxes = [cv.boundingRect(i) for i in contours]

# 找最小外接矩形
rect = cv2.minAreaRect(contours[2])      # 返回矩形的中心点坐标，长宽，旋转角度[-90,0)，当矩形水平或竖直时均返回-90


# 绘制带角度的矩形
box = cv2.boxPoints(rect)                                      # 先提取点集
cv2.drawContours(img_1, [np.int0(box)], 0, (0,0,255), 5)       # 再绘制图像
cv2.polylines(img_1, [np.int0(box)], True, (255,0,0), 5)       # 也可用此函数绘制图像

# minEnclosingCircle() 找外接圆
center, radius = cv2.minEnclosingCircle(contours[4])  # points输入的二维点集  返回圆心、半径
cv2.circle(img_1, (int(center[0]), int(center[1])), radius=int(radius), color=(45,100,200))

# fitEllipse() 找最小外接矩形的内接椭圆
centerCoordinates = cv2.fitEllipse(contours[3])  # 返回((椭圆中心坐标),(长轴,短轴),旋转角度)
# 绘制椭圆
cv2.ellipse(img_1, (int(centerCoordinates[0][0]), int(centerCoordinates[0][1])), (int(centerCoordinates[1][0]),
                    int(centerCoordinates[1][1])), centerCoordinates[2], 0, 360, (45,150,100), 1)

# 计算椭圆离心率、圆滑度
axis_l = max(centerCoordinates[1][0], centerCoordinates[1][1])  # 长轴
axis_s = min(centerCoordinates[1][0], centerCoordinates[1][1])  # 短轴
eccentricity = math.sqrt(1-pow(axis_s/axis_l, 2))  # 离心率
roundness = (4*math.pi*cv2.contourArea(contours[3])) / pow(cv2.arcLength(contours[3], True), 2)  # 圆滑度
print('离心率：', eccentricity, '\n', '圆滑度：', roundness)

# fitLine() 由点集拟合直线
ret_line = cv2.fitLine(contours[3], cv2.DIST_L2, 0, 0.01, 0.01)  # 点集 距离类型 距离参数(0表示函数自动选择) 径向精度 角度精度  返回值：方向矢量 线上一点
k = ret_line[1] / ret_line[0]  # 直线斜率
point0 = [ret_line[2], ret_line[3]]
point1 = (120, int(k * (120 - point0[0]) + point0[1]))
point2 = (150, int(k * (150 - point0[0]) + point0[1]))
cv2.line(img_1, point1, point2, (120,255,180), 1)


# 显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig,axes=plt.subplots(nrows=2,ncols=3,figsize=(10,8),dpi=100)   # figsize 窗口长宽比  dpi 字体大小
axes[0][0].imshow(result, plt.cm.gray)
axes[0][0].set_title('Sobel检测')
axes[0][1].imshow(result2, plt.cm.gray)
axes[0][1].set_title('Scharr检测')
axes[0][2].imshow(result3, plt.cm.gray)
axes[0][2].set_title('Laplacian检测')
axes[1][0].imshow(result4, plt.cm.gray)
axes[1][0].set_title('Canny边缘检测（推荐）')
axes[1][1].imshow(img_1[:,:,::-1])
axes[1][1].set_title('轮廓检测')
axes[1][2].imshow(img_final[:,:,::-1])
axes[1][2].set_title('扣出目标轮廓')
plt.show()
