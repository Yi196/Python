import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

img = cv2.imread(r'./image/003.jpg')
img_1 = img.copy()
img_2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.minMaxLoc(a)获取矩阵的最小值、最大值及对应索引
a=np.array([[1,2,3,4],[5,67,8,9]])
min_val, max_val, min_indx, max_indx = cv2.minMaxLoc(a)
print(min_val, max_val, min_indx, max_indx)  # 1.0 67.0 (0, 0) (1, 1)


# cv2.countNonZero()：返回灰度值不为0的像素数，可用来判断图像是否全黑
print(cv2.countNonZero(a))  # 8


# cv2.subtract(binary, temp),矩阵相减，获取两图片不同之处
b=np.array([[0, 1, 2, 3],[4, 56, 7, 8]])
print(cv2.subtract(a, b))


# 图像通道的分离（split（）函数）和合并（merge（）函数）
B,G,R = cv2.split(img)
zeros = np.zeros_like(B,np.uint8)
img_red = cv2.merge([zeros,zeros,R])
img_green = cv2.merge([zeros,G,zeros])
img_blue = cv2.merge([B,zeros,zeros])

fig,axes=plt.subplots(nrows=1,ncols=4,figsize=(10,8),dpi=100)
axes[0].imshow(B,plt.cm.gray)
axes[1].imshow(img_red[:,:,::-1])
axes[2].imshow(img_green[:,:,::-1])
axes[3].imshow(img_blue[:,:,::-1])
plt.show()


'''
#opencv和PIL图像间转换
# opencv -> pil
img_cv = None
img_pil = Image.fromarray(cv2.cvtColor(img_cv,cv2.COLOR_BGR2RGB))

# pil -> opencv
img_cv = cv2.cvtColor(np.asarray(img_pil),cv2.COLOR_RGB2BGR)
'''


# 通过cv2.applyColorMap()函数，我们可以将灰度图转换成红色-蓝色的热力图，当值为255时，为红色，当值为0时，为蓝色
img_gray = cv2.imread(r'./image/006.jpg',0)
heat_img = cv2.applyColorMap(img_gray, cv2.COLORMAP_JET)
cv2.imshow('',heat_img)
cv2.waitKey(0)


# 将二值化图转换成距离灰度图(距离变换函数cv2.distanceTransform()的计算结果反映了各个像素与背景（值为 0 的像素点）的距离关系)
img_gray = cv2.imread(r'./image/003.jpg',0)
_, binary = cv2.threshold(img_gray,90,255,cv2.THRESH_BINARY)
# binary = cv2.bitwise_not(binary)
dist = cv2.distanceTransform(src=binary, distanceType=cv2.DIST_L2, maskSize=5)
dist1 = cv2.convertScaleAbs(dist)  # 注意要用该函数将结果转为uint8格式才能显示
# 归一化
dist2= cv2.normalize(dist, None, 255,0, cv2.NORM_MINMAX, cv2.CV_8UC1)  # 将矩阵值转为0至255
heat_img = cv2.applyColorMap(dist2, cv2.COLORMAP_JET)
cv2.imshow('',heat_img)
cv2.waitKey(0)

# 计算全局均值、标准差
mean_global, var_global = cv2.meanStdDev(img)


# 计算点到直线距离
def point_distance_line(point,line_point1,line_point2):
    # 计算向量
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(line_point1 - line_point2)
    return distance


# 计算X/Y方向直线的边数 各边中点坐标(边必须为轴向的)
def num_lines(binary,num_line,num_ignore,is_X=True):
    '''
    binary: 处理后的二值化图像
    num_line: 像素大于一定数量才被视为线
    num_ignore: 当两条线间距小于num_ignore个像素时 被视为一条线
    is_X: 计算X方向
    '''
    sum_binary = np.sum(binary, axis=1 if is_X else 0)
    the_sum = sum_binary > num_line * 255
    # 判断直线连续
    l = []
    ll = []
    for i in range(len(the_sum)):
        if the_sum[i] == True:
            ll.append(i)
        else:
            if len(ll) > 0:
                l.append(ll)
                ll = []
    if len(ll) != 0:
        l.append(ll)

    # 判读两直线间是否较近
    del_lst = []
    for i in range(len(l) - 1):
        if l[i+1][0]-l[i][-1] < num_ignore + 1:
            del_lst.append(i)

    # 将相距较近的线合并为一条直线
    for i in del_lst[::-1]:
        l_i_1 = l[i + 1]
        l_i = l[i]
        l.pop(i + 1)
        l.pop(i)
        l.insert(i, [i for i in range(l_i[0], l_i_1[-1] + 1)])

    # 返回X/Y方向直线 数量
    # return len(l)

    centers = [sum(i)/len(i) for i in l]
    # 返回每条线中线坐标(X方向直线为Y坐标)
    return centers

np.hstack([img,np.stack([binary,binary,binary],axis=-1)])  # 合并两张图像

# 图像增强
# 1、求梯度
def get_grad(img):
    img = cv2.bilateralFilter(img, 7, 75, 75)
    grad_x = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    grad_y = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    gradx = cv2.convertScaleAbs(grad_x)
    grady = cv2.convertScaleAbs(grad_y)
    img_ret = cv2.addWeighted(gradx, 0.5, grady, 0.5, 0)
    return img_ret
# 2、自适应直方图均衡化
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
img_clahe = clahe.apply(img_2)
# 3、像素值乘某个值(较暗时提高像素差)
img_out = img_gray * 3
img_out[img_out > 255] = 255
img_out.astype(np.uint8)  # img_out = np.around(img_out)
# 4、让一幅图像加上它的Laplacian算子可以 锐化图像
laplac = cv2.Laplacian(img_1, cv2.CV_16S)  #cv.CV_16S用于转换数字类型 避免结果溢出
result3 = cv2.convertScaleAbs(laplac)      #数据转换为 np.uint8
img_ret = 0.5 * img + 0.5 * result3
cv2.imshow('',img_ret)
cv2.waitKey(0)