import cv2,os
import numpy as np


img = cv2.imread(r'./image/010.png')

# 图像增强方法
# 1、灰度变换
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height = img_gray.shape[0]
width = img_gray.shape[1]

# 1.1 线性变换（利用线性函数拉伸和压缩目标区域、反转颜色（255-X））
# 反转颜色
reverse = 255 - img_gray
cv2.imshow('reverse',reverse)
# 灰度值上移  DB = DA + 50
gray_up = np.zeros_like(img_gray, np.uint8)
for y in range(height):
    for x in range(width):
        if (int(img_gray[y, x] + 50) > 255):
            gray = 255
        else:
            gray = int(img_gray[y, x] + 50)
        gray_up[y, x] = np.uint8(gray)
cv2.imshow('up', gray_up)
# 图像拉伸  DB = DA * 1.5
gray_thretch = np.zeros_like(img_gray, np.uint8)
for y in range(height):
    for x in range(width):
        if (int(img_gray[y, x] * 1.5) > 255):
            gray = 255
        else:
            gray = int(img_gray[y, x] * 1.5)
        gray_thretch[y, x] = np.uint8(gray)
cv2.imshow('thretch', gray_thretch)
# 图像压缩  DB = DA * 0.8
gray_compress = np.zeros_like(img_gray, np.uint8)
for y in range(height):
    for x in range(width):
        gray = int(img_gray[y, x] * 0.8)
        gray_compress[y, x] = np.uint8(gray)
cv2.imshow('compress', gray_compress)


# 1.2 非线性变换
# 图像灰度非线性变换  DB = DA * DA / 255
gray_non_liner = np.zeros_like(img_gray, np.uint8)
for i in range(height):
    for j in range(width):
        gray = int(img_gray[i, j]) * int(img_gray[i, j]) / 255
        gray_non_liner[i, j] = np.uint8(gray)
cv2.imshow('non_liner', gray_non_liner)


# 1.2.1对数变换（暗区拉伸 适用于窄带低灰度图像） DB = c * log(1 + DA)
def log(c, img):
    output = c * np.log(1.0 + img)
    output = np.uint8(output + 0.5)
    return output
img_log_25 = log(25, img)
img_log_35 = log(35, img)
img_log_42 = log(42, img)
cv2.imshow('log_25', img_log_25)
cv2.imshow('log_35', img_log_35)
cv2.imshow('log_42', img_log_42)


# 1.2.2幂次变换(伽玛变换)（亮区拉伸 适用于高灰度图像） DB = c * DA ** gamma (gamma<1时也可起到暗区拉伸作用)
def gamma(img, c, gamma):
    # 映射表必须为0~255(改成其他会报错）
    gamma_table = c * [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    output_img = cv2.LUT(img, gamma_table)
    return output_img
def gamma_1(img, c, gamma):
    output_img = c * np.power(img / float(np.max(img)), gamma) * 255.0
    output_img = np.uint8(output_img)
    return output_img

img_gamma_LUT = gamma(img_gray, 1, 2)
img_gamma = gamma_1(img_gray, 1, 2)
cv2.imshow('gamma_LUT', img_gamma_LUT)
cv2.imshow('gamma', img_gamma)

# 1.2.3直方图均衡(用于曝光过度、不足 提高对比度)
equ_img = cv2.equalizeHist(img_gray)
cv2.imshow('equ_img', equ_img)
# 自适应直方图均衡化
clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8, 8))   # clipLimit=2.0对比度限制 默认40 常用2.0 3.0 4.0    tileGridSize=(8,8)分块的小 默认8X8
clahe_img = clahe.apply(img_gray)  # 注意为单通道灰度图
cv2.imshow('clahe_img', clahe_img)


# 2、代数运算
'''注意加减时要使用cv2.add()、cv2.subtract(),否则会出现结果溢出发生反转'''
# 2.1加法运算（两幅或多幅图相加：去除叠加性噪声（相当与求均值））
''' img_ret = 0.05*img1 + 0.05*img2 + ... + 0.05*img20
np.uint8(img_ret)'''
# 2.2减法运算（两幅图像相减再二值：分割特定区域、检测场景变化）
''' img_ret = cv2.subtract(img1, img2)
_, binary = cv2.threshold(img_ret, 5, 255, cv2.THRESH_BINARY)'''
# 2.3乘法运算（做掩膜）
mask = np.zeros_like(img_gray)
mask[img_gray > 230] = 1
img_mask = img_gray * mask
cv2.imshow('mask', img_mask)


# 3、空间域滤波
# 3.1图像平滑（低通滤波）
# 均值滤波 核内求平均 会弱化边缘
img_blur = cv2.blur(img, ksize=(3, 3))
cv2.imshow('blur', img_blur)
# 高斯滤波 核内求加权平均 使图像平滑
img_gauss = cv2.GaussianBlur(img, ksize=(3, 3), sigmaX=1)
cv2.imshow('gauss', img_gauss)
# 中值滤波  对核内像素值排序取中值 可有效去除突出的亮暗点 保留边缘
img_median = cv2.medianBlur(img, ksize=3)
cv2.imshow('median', img_median)
# 双边滤波  保边降噪
img_bilateral = cv2.bilateralFilter(img, 5, 30, 30)
cv2.imshow('bilateral', img_bilateral)

# NLM非局部均值 去除高斯噪声
img_opencv_nlm = cv2.fastNlMeansDenoising(img_gray, None, 18, 7, 21)
# from _28NLM非局部均值算法 import NLmeansfilter
# img_nlm = NLmeansfilter(img_gray)
# cv2.imshow('img_opencv_nlm', img_opencv_nlm)


img_rh = cv2.imread(r'./image/ruihua.png')
# 3.2图像锐化（高通滤波）
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 锐化
img_dst = cv2.filter2D(img_rh, -1, kernel=kernel)
cv2.imshow('dst', img_dst)
# 3.2.1Sobel算子（一阶差分）：对噪声敏感度较低，可以检测边缘方向，无法进行边缘定位（判断像素点在边缘内外测）
'''黑色到白色的过渡被视为正斜率（具有正值），而白色到黑色的过渡被视为负斜率（具有负值）。输出设置为CV_8U会丢失负值。
如果要检测两个边缘，更好的选择是将输出数据类型保留为更高的形式，例如CV_16S，CV_64F等，取其绝对值，然后转换回CV_8U。'''
# Sobel_8U
sobel_dx = cv2.Sobel(img_rh, cv2.CV_8U, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
sobel_dy = cv2.Sobel(img_rh, cv2.CV_8U, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
ret = cv2.addWeighted(sobel_dx, 0.5, sobel_dy, 0.5, 0)
img_sobel_8u = cv2.addWeighted(ret, 1, img_rh, 1, 0)
cv2.imshow('Sobel_8u', img_sobel_8u)
# Sobel_16S
sobel_dx = cv2.Sobel(img_rh, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
sobel_dy = cv2.Sobel(img_rh, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
ret = cv2.addWeighted(cv2.convertScaleAbs(sobel_dx), 0.5, cv2.convertScaleAbs(sobel_dy), 0.5, 0)
img_sobel_16s = cv2.addWeighted(ret, 0.5, img_rh, 1, 0)
cv2.imshow('Sobel_16s', img_sobel_16s)


# 3.2.2Laplace算子（二阶差分）：对噪声敏感，不能检测边缘的方向，零交叉性质进行边缘定位
img_blur = cv2.GaussianBlur(img_rh, (3, 3), 1)
laplac = cv2.Laplacian(img_blur, cv2.CV_16S)
laplacian = cv2.convertScaleAbs(laplac)
img_laplacian = cv2.addWeighted(laplacian, 1.5, img_rh, 1, 0)
cv2.imshow('Laplacian', img_laplacian)


# 3.2.3Roberts算子  通过交叉微分检测局部变化，边缘定位精度较高，但容易丢失一部分边缘
# Roberts_8U
kernel_1 = np.array([[1,0], [0,-1]], np.float32)
kernel_2 = np.array([[0,1], [-1,0]], np.float32)
img_dst1 = cv2.filter2D(img_rh, -1, kernel=kernel_1)
img_dst2 = cv2.filter2D(img_rh, -1, kernel=kernel_2)
ret = cv2.addWeighted(img_dst1, 0.5, img_dst2, 0.5, 0)
img_roberts_8u = cv2.addWeighted(ret, 1, img_rh, 1, 0)
cv2.imshow('Roberts_8u', img_roberts_8u)
# Roberts_16S
img_dst1 = cv2.filter2D(img_rh, cv2.CV_16S, kernel=kernel_1)
img_dst2 = cv2.filter2D(img_rh, cv2.CV_16S, kernel=kernel_2)
ret = cv2.addWeighted(cv2.convertScaleAbs(img_dst1), 1, cv2.convertScaleAbs(img_dst2), 1, 0)
img_roberts_16s = cv2.addWeighted(ret, 1, img_rh, 1, 0)
cv2.imshow('Roberts_16s', img_roberts_16s)



# 4、频域滤波(傅里叶变换) 空间域的卷积等于频域的乘积 反之亦然  Butterworth、高斯滤波器(无振铃现象)
from _18高低通滤波_傅里叶变换 import fft_img
# 4.1低通滤波(图像平滑) (图像上有栅格)
# 4.2高通滤波(图像锐化) 高斯高通滤波效果更好 (X光照可先高通滤波保留细节，再直方图均衡)
img_fft_high = fft_img(cv2.cvtColor(img_rh,cv2.COLOR_BGR2GRAY), 8, is_high=True)
img_fft = cv2.addWeighted(cv2.merge([img_fft_high]*3), 0.5, img_rh, 1, 0)
cv2.imshow('fft_high', img_fft)

# 4.3同态滤波(用于光照不均匀)：衰减低频（照射分量）的贡献，而增强高频（反射分量）的贡献。最终结果是同时进行动态范围的压缩和对比度的增强
# 基于Retinex滤波
from _23同态滤波_Retinex import my_homofilter
# img_rx = cv2.imread('./image/tongtai.jpg')
# img_Retinex = my_homofilter(img_rx)
# cv2.namedWindow('Retinex', 0)
# cv2.imshow('Retinex', img_Retinex)


cv2.waitKey(0)