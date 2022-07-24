import cv2, os
import numpy as np


def detect_wpoint(img:list)->bool:
    image = img.copy()
    # 提取陶瓷片区域
    img_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower = np.array([0, 52, 122])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(img_hsv, lower, upper)
    image[mask==0] = 0
    # cv2.imshow('', image)
    # cv2.waitKey(0)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 提高对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_img = clahe.apply(image)

    # 二值判断白点数量
    _, binary = cv2.threshold(clahe_img,153,255,cv2.THRESH_BINARY)

    cv2.imshow('',binary)
    cv2.waitKey(0)

    count_w = len(binary[binary==255])
    if count_w > 12000:
        return False
    else:
        return True


if __name__ == '__main__':
    # dir = r'C:\Users\dihuge\Desktop\000'
    # names = os.listdir(dir)
    # for name in names:
    #     img = cv2.imread(os.path.join(dir,name))
    #     print(detect_wpoint(img))
    print(detect_wpoint(cv2.imread(r'./template/001.png')))