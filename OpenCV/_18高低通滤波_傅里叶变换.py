import cv2
import numpy as np
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimHei']

# 使用高通滤波器之后，会保留高频信息，增强图像细节，例如边界增强
# 使用低通滤波器之后，会保留低频信息，边界模糊
def fft_img(src, threshold=30, is_high=True):
    if len(src.shape) != 2:
        src = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    # 进行傅里叶变换
    fft = cv2.dft(np.float32(src), flags=cv2.DFT_COMPLEX_OUTPUT)   # 需要将图像进行一次float转换

    # 将低频部分移至图像中心（通过掩掉中间位置或四周实现高低通滤波）
    fshift = np.fft.fftshift(fft)

    # 频谱图像双通道复数转换为 0-255 区间 可用于显示频谱图像
    # result1 = 20 * np.log(cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1]))
    # result1 = (result1 / result1.max() * 255).astype(np.uint8)

    rows, cols = src.shape
    crow, ccol = rows//2, cols//2
    if is_high:
        # 高通滤波掩膜
        fshift[int(crow - threshold):int(crow + threshold), int(ccol - threshold):int(ccol + threshold)] = 0
    else:
        # 低通滤波掩膜
        mask = np.zeros((rows,cols,2), np.uint8)   # opencv中复数 第三维有两个元素
        mask[int(crow - threshold):int(crow + threshold), int(ccol - threshold):int(ccol + threshold)] = 1
        fshift = fshift * mask

    # 傅里叶逆变换
    ifshift = np.fft.ifftshift(fshift)
    ifft = cv2.idft(ifshift)
    # 将复数转为0-255整数
    ifft_img = cv2.magnitude(ifft[:,:,0],ifft[:,:,1])     # 求平方和，再开根号 此处为求复数的模
    ifft_img = (ifft_img/ifft_img.max() * 255).astype(np.uint8)

    return ifft_img


if __name__ == '__main__':
    src = cv2.imread(r'./image/001.jpg', 0)
    img = fft_img(src, 10, is_high=True)
    # print(img)
    cv2.imshow('', img)
    cv2.waitKey(0)

    # plt用于显示输出图像矩阵为 复数的模
    # plt.subplot(111), plt.imshow(img, 'gray'), plt.title('傅里叶变换')
    # plt.axis('off')
    # plt.show()