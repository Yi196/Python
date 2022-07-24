import cv2
import numpy as np


# 基于图像标记(mark)的分水岭算法 将图像分割为标记好的不同区域
def watershed(img):
    '''
    img: 三通道图像
    '''
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img[:, :, 0]
    else:
        gray = img
        img = cv2.merge([img]*3)

    # 图像预处理
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_open = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # 制作mark，指明 前景(>1) 背景(1) 不确定区域(0)（前背景边缘所在区域）
    # 法一：腐蚀得到前景，膨胀-腐蚀为不确定区域
    # foreground = cv2.erode(img_open, kernel, iterations=2)
    # background = cv2.dilate(img_open, kernel, iterations=2)
    # unknow = cv2.subtract(background, foreground)
    # 法二：当腐蚀无法获取前景区域时，可使用距离变换
    dist_transf = cv2.distanceTransform(img_open, cv2.DIST_L2, 5)
    dist_transf = cv2.normalize(dist_transf, None, 0,1.0,cv2.NORM_MINMAX) # 归一化
    _, foreground = cv2.threshold(dist_transf, 0.5*dist_transf.max(), 255, 0)
    foreground = np.uint8(foreground)
    background = cv2.dilate(img_open, kernel, iterations=2)
    unknow = cv2.subtract(background, foreground)

    # 可通过cv2.connectedComponents()生成mark,它使用前景(>0) 背景(0)
    _, markers = cv2.connectedComponents(foreground)
    markers = markers + 1 # 使markers变为分水岭算法mark
    markers[unknow==255] = 0

    # 使用分水岭算法
    markers = cv2.watershed(img, markers)
    # 返回的markers 分水岭算法会将找到的栅栏设置为-1 （背景1，前景>1,无0）

    # 显示
    img_show = np.zeros_like(img)
    min_val, max_val, min_indx, max_indx = cv2.minMaxLoc(markers)
    # 显示分割区域
    for i in range(2, int(max_val + 1)):
        img_show[:, :, 0][markers == i] = np.random.randint(0, 255)
        img_show[:, :, 1][markers == i] = np.random.randint(0, 255)
        img_show[:, :, 2][markers == i] = np.random.randint(0, 255)

    cv2.imshow('img_region', img_show)

    # 显示边缘
    img[markers == -1] = [0, 0, 255]
    cv2.imshow('img_edge', img)
    cv2.waitKey(0)

    return markers

if __name__ == '__main__':
    img = cv2.imread(r'./image/watershed.jpg')
    markers = watershed(img)
    print(markers)