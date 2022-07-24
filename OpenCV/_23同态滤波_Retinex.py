import cv2
import numpy as np


'''同态滤波的目的：消除不均匀照度的影响而又不损失图象细节。其依据：图象的灰度由照射分量和反射分量合成。 反射分量反映图象内容，
随图象细节不同在空间上作快速变化。照射分量在空间上通常均具有缓慢变化的性质。照射分量的频谱落在空间低频区域，反射分量的频谱落在空间高频区。
同态滤波(用于光照不均匀)：衰减低频（照射分量）的贡献，而增强高频（反射分量）的贡献。最终结果是同时进行动态范围的压缩和对比度的增强'''

def my_homofilter(img, gammaL = 0.5, gammaH = 5, C = 3, d0 = 9):
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img = img[:, :, 0]

    img = np.float32(img)
    rows, cols = img.shape

    # 1、取对数
    img_log = np.log(img + 1)
    # 2、傅里叶变换
    fft = np.fft.fft2(img_log)
    # 3、频域滤波
    n1 = np.floor(rows / 2)
    n2 = np.floor(cols / 2)
    H = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            d2 = (i - n1) ** 2 + (j - n2) ** 2
            H[i, j] = (gammaH - gammaL) * np.exp(C * (-d2 / (d0 ** 2))) + gammaL  # %高斯同态滤波
    # print('H', H)

    # 傅里叶逆变换
    ifft = np.fft.ifft2(H * fft)
    # 指数运算
    img_exp = np.exp(ifft)
    # 将复数转为0-255整数
    ifft_img = cv2.magnitude(np.real(img_exp), np.imag(img_exp))  # 求平方和，再开根号 此处为求复数的模
    ifft_img = (ifft_img / ifft_img.max() * 255).astype(np.uint8)
    return ifft_img


def my_homofilter_RGB(img, gammaL = 0.5, gammaH = 5, C = 3, d0 = 9):
    B, G, R = cv2.split(img)
    img_ret_B = my_homofilter(B, gammaL, gammaH, C, d0)
    img_ret_G = my_homofilter(G, gammaL, gammaH, C, d0)
    img_ret_R = my_homofilter(R, gammaL, gammaH, C, d0)
    img_ret = cv2.merge([img_ret_B, img_ret_G, img_ret_R])
    return img_ret


if __name__ == '__main__':
    img = cv2.imread(r'./image/tongtai.jpg')

    img_ret = my_homofilter(img)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)
    cv2.namedWindow('ret', cv2.WINDOW_NORMAL)
    cv2.imshow('ret', img_ret)


    img_ret_RGB = my_homofilter_RGB(img)
    cv2.namedWindow('ret_RGB', cv2.WINDOW_NORMAL)
    cv2.imshow('ret_RGB', img_ret_RGB)
    cv2.waitKey(0)
