import cv2
import numpy as np
import math


'''
ACE在图像处理方面可以有两种表示，一种是Automatic Color Equalization，即自动彩色均衡；还有一种是Adaptive Contrast Enhancement，即自适应对比度增强
依据Retinex理论提出了自动颜色均衡算法，该算法考虑了图像中颜色和亮度的空间位置关系，进行局部特性的自适应滤波，实现具有局部和非线性特征的图像亮度与色彩调整和对比度调整，同时满足灰色世界理论假设和白色斑点假设。
'''


def stretchImage(data, s=0.005, bins=2000):  # 线性拉伸，去掉最大最小0.5%的像素值，然后线性拉伸至[0,1]
    # 统计给阶段象素所占百分比
    ht = np.histogram(data, bins)
    d = np.cumsum(ht[0]) / float(data.size)
    lmin = 0
    lmax = bins - 1
    while lmin < bins:
        if d[lmin] >= s:
            break
        lmin += 1
    while lmax >= 0:
        if d[lmax] <= 1 - s:
            break
        lmax -= 1
    return np.clip((data - ht[1][lmin]) / (ht[1][lmax] - ht[1][lmin]), 0, 1)


g_para = {}


def getPara(radius=5):  # 根据半径计算权重参数矩阵
    global g_para
    m = g_para.get(radius, None)
    if m is not None:
        return m
    size = radius * 2 + 1
    m = np.zeros((size, size))
    for h in range(-radius, radius + 1):
        for w in range(-radius, radius + 1):
            if h == 0 and w == 0:
                continue
            m[radius + h, radius + w] = 1.0 / math.sqrt(h ** 2 + w ** 2)
    m /= m.sum()
    g_para[radius] = m
    return m


def zmIce(I, ratio=4, radius=3):  # 常规的ACE实现
    para = getPara(radius)
    height, width = I.shape
    # 填充边界 以用于卷积
    # zh, zw = [0] * radius + list(range(height)) + [height - 1] * radius, [0] * radius + list(range(width)) + [width - 1] * radius
    # Z = I[np.ix_(zh, zw)]
    Z = np.pad(I, ((radius,radius), (radius,radius)), 'edge')  # 与上式等效
    res = np.zeros(I.shape)
    for h in range(radius * 2 + 1):
        for w in range(radius * 2 + 1):
            if para[h][w] == 0:
                continue
            res += (para[h][w] * np.clip((I - Z[h:h + height, w:w + width]) * ratio, -1, 1))
    return res


def zmIceFast(I, ratio, radius):  # 单通道ACE快速增强实现
    height, width = I.shape[:2]
    if min(height, width) <= 2:
        return np.zeros(I.shape) + 0.5
    Rs = cv2.resize(I, ((width + 1) // 2, (height + 1) // 2))
    Rf = zmIceFast(Rs, ratio, radius)  # 递归调用
    Rf = cv2.resize(Rf, (width, height))
    Rs = cv2.resize(Rs, (width, height))

    return Rf + zmIce(I, ratio, radius) - zmIce(Rs, ratio, radius)


def zmIceColor(I, ratio=4, radius=3):
    '''
    rgb三通道分别增强，
    I:输入图像
    ratio:是对比度增强因子
    radius:是卷积模板半径
    '''
    assert I is not None, "img is not None!"

    assert len(I.shape) > 2, "img most RGB"

    res = np.zeros(I.shape)
    I = I / 255.0
    for k in range(3):
        res[:, :, k] = stretchImage(zmIceFast(I[:, :, k], ratio, radius))
    return np.uint8(res*255)


if __name__ == '__main__':
    img = cv2.imread(r'./image/005.jpg')
    m = zmIceColor(img)
    cv2.imshow('img', m)
    cv2.waitKey(0)
