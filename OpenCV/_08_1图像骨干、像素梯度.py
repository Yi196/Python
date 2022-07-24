import numpy as np
import cv2


def skelenton(binary):
    '''生成一个二值化图像的骨架'''

    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    skel = np.zeros_like(binary,np.uint8)

    while True:
        eroded = cv2.erode(binary, element)
        temp = cv2.dilate(eroded, element)

        # 消失的像素是skeleton的一部分
        temp = cv2.subtract(binary, temp)
        skel = cv2.bitwise_or(skel, temp)
        binary = eroded.copy()

        if cv2.countNonZero(binary) == 0:
            break
    return skel


def gen_magnitude(img):
    '''
    计算图像的梯度特征
    :param img:
    :return:
    '''
    smoothed = cv2.GaussianBlur(img, (3, 3), 0, sigmaY=0, borderType=cv2.BORDER_REPLICATE)
    sobel_dx = cv2.Sobel(smoothed, cv2.CV_32F, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    sobel_dy = cv2.Sobel(smoothed, cv2.CV_32F, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    # 计算像素梯度的绝对值
    magnitude = cv2.magnitude(sobel_dx, sobel_dy)   # 求平方和，再开根号
    # magnitude = np.sqrt(sobel_dx * sobel_dx + sobel_dy * sobel_dy)

    # 计算像素梯度的方向
    sobel_ag = cv2.phase(sobel_dx, sobel_dy, angleInDegrees=True)  #angleInDegrees=True表示结果用角度制表示，否则用弧度制

    return magnitude, sobel_ag



if __name__ == '__main__':
    img = cv2.imread(r'./image/003.jpg',0)
    ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    skeleton = skelenton(binary)

    magnitude, sobel_ag = gen_magnitude(img)

    # hist_img = cv2.calcHist([sobel_ag.ravel()], [0], None, [256], [0, 256])

    for i in [skeleton,magnitude, sobel_ag]:
        cv2.imshow('',i)
        cv2.waitKey(0)