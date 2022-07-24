import cv2
import numpy as np


'''
NML:Non-Local Means利用了整幅图像来进行去噪，以图像块为单位在图像中寻找相似区域，再对这些区域求平均，能够比较好地去掉图像中存在的高斯噪声
'''

# 产生高斯噪声
def img_nois(img, sigma=20, ratio=1.0):
    return np.clip(np.round((img + np.random.randn(*img.shape)*sigma)*ratio), 0, 255).astype(np.uint8)
img = cv2.imread(r'./image/005.jpg', 0)
cv2.imshow('img', img)
img_n = img_nois(img)
cv2.imshow('img_nois', img_n)

# opencv中API
'''
cv2.fastNlMeansDenoising() - 使用单个灰度图像
cv2.fastNlMeansDenoisingColored() - 使用彩色图像。
cv2.fastNlMeansDenoisingMulti() - 用于在短时间内捕获的图像序列（灰度图像） (类似多张图相加求平均降噪)
cv2.fastNlMeansDenoisingColoredMulti() - 与上面相同，但用于彩色图像。
• h : 决定过滤器强度。h 值高可以很好的去除噪声,但也会把图像的细节抹去。(取 10 的效果不错)
• hForColorComponents : 与 h 相同,但使用与彩色图像。(与 h 相同,10)
• templateWindowSize : 奇数。(推荐值为 7)
• searchWindowSize : 奇数。(推荐值为 21)
'''
img_opencv_nlm = cv2.fastNlMeansDenoising(img_n, None, 20, 5, 11)
cv2.imshow('img_opencv_nlm', img_opencv_nlm)


# 自实现NLM算法
def NLmeansfilter(I, h_=10, templateWindowSize=5,  searchWindowSize=11):
    I = I.astype(np.double)
    f = int(templateWindowSize/2)
    t = int(searchWindowSize/2)
    height, width = I.shape[:2]
    padLength = int((templateWindowSize + searchWindowSize)/2)
    I2 = np.pad(I, padLength, 'symmetric')

    kernel = np.zeros((2*f+1, 2*f+1))
    for d in range(1, f+1):
        kernel[f-d:f+d+1, f-d:f+d+1] += (1.0/((2*d+1)**2))
    kernel = kernel/kernel.sum()
    h = (h_**2)
    I_ = I2[padLength-f:padLength+f+height, padLength-f:padLength+f+width]

    average = np.zeros(I.shape)
    sweight = np.zeros(I.shape)
    wmax =  np.zeros(I.shape)
    for i in range(-t, t+1):
        for j in range(-t, t+1):
            if i==0 and j==0:
                continue
            I2_ = I2[padLength+i-f:padLength+i+f+height, padLength+j-f:padLength+j+f+width]
            w = np.exp(-cv2.filter2D((I2_ - I_)**2, -1, kernel)/h)[f:f+height, f:f+width]
            sweight += w
            wmax = np.maximum(wmax, w)
            average += (w*I2_[f:f+height, f:f+width])
    return np.clip(((average+wmax*I)/(sweight+wmax)), 0, 255).astype(np.uint8)


img_nlm = NLmeansfilter(img_n, 20, 5, 11)
cv2.imshow('img_nlm', img_nlm)


# 评价函数
def psnr(A, B):
    return 10*np.log10(255*255.0/(((np.double(A)-B)**2).mean()))

print('噪声图像PSNR', psnr(img, img_n))

img_blur = cv2.medianBlur(img_n, 5)
cv2.imshow('中值滤波图象', img_blur)
print('中值滤波PSNR', psnr(img, img_blur))

print('opencv的NLM算法', psnr(img, img_opencv_nlm))

print(u'NLM PSNR', psnr(img, img_nlm))

cv2.waitKey(0)