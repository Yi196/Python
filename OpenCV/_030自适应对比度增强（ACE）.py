import cv2
import numpy as np
import math


def AdaptiveContrastEnhancement(img, ksize=7, C=5, max_C=8):
    '''
    ksize: 计算局部均值、表均差时的区域大小
    C: 对高频的直接增益系数
    max_C: 对高频成分的最大增益值
    '''

    # 计算局部均值
    mean_local = cv2.blur(img, (ksize,ksize))
    # 计算局部标准差
    '''注意此处只能使用cv2.subtract(),否则会出现相减结果为负时，反转为255'''
    highfreq = cv2.subtract(img, mean_local)         # 先提取高频成分
    var_local = cv2.multiply(highfreq, highfreq)
    var_local = cv2.blur(var_local, (ksize, ksize))  # 计算局部方差
    var_local = np.sqrt(var_local)                   # 计算局部标准差

    # 计算全局均值、标准差
    mean_global, var_global = cv2.meanStdDev(img)

    # 计算增益系数矩阵
    enhance_arr = 0.5 * np.divide(mean_global, var_local, out=np.zeros_like(var_local, dtype=np.float64), where=var_local!=0)
    enhance_arr = np.clip(enhance_arr, None, max_C).astype(np.uint8)  # 截断
    enhance_arr = cv2.multiply(enhance_arr, highfreq)

    # 变增益方法
    dst1 = cv2.add(mean_local, enhance_arr)
    cv2.imshow('变增益方法', dst1)

    # 恒增益方法
    dst2 = cv2.add(mean_local, C * highfreq)
    cv2.imshow('恒增益方法', dst2)
    cv2.waitKey(0)


if __name__ == '__main__':
    img = cv2.imread(r'./image/005.jpg', 0)
    AdaptiveContrastEnhancement(img)