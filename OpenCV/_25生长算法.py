import numpy as np
import cv2
import matplotlib.pyplot as plt

# 生长算法：用于灰度范围较大且灰度逐渐变化
'''确定种子像素：人机交互式分割、基于直方图的粗分割结果作为种子
确定相似性：基于区域灰度差、基于区域灰度分布统计性质'''

# 基于区域灰度差确定相似性
def getGrayDiff(img, currentPoint, tmpPoint):
    return abs(int(img[currentPoint[1], currentPoint[0]]) - int(img[tmpPoint[1], tmpPoint[0]]))


def selectConnects(p):
    if p != 0:
        connects = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
    else:
        connects = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    return connects


def regionGrow(img, seeds, thresh, p=1):
    '''
    seeds: 种子像素位置
    thresh: 区域灰度差 小于阈值视为同一区域
    p: 生长方向 p=0时仅轴向生长
    '''
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img = img[:, :, 0]

    height, weight = img.shape
    seedMark = np.zeros_like(img)
    label = 255
    connects = selectConnects(p)
    while (len(seeds) > 0):
        currentPoint = seeds.pop(0)

        seedMark[currentPoint[1], currentPoint[0]] = label
        for i in range(len(connects)):
            tmpX = currentPoint[0] + connects[i][0]
            tmpY = currentPoint[1] + connects[i][1]
            if tmpX < 0 or tmpY < 0 or tmpY >= height or tmpX >= weight:
                continue
            if seedMark[tmpY, tmpX] != 0:
                continue
            grayDiff = getGrayDiff(img, currentPoint, [tmpX, tmpY])
            if grayDiff < thresh:
                seedMark[tmpY, tmpX] = label
                seeds.append([tmpX, tmpY])
                cv2.imshow('ret', seedMark)
                cv2.waitKey(1)
    return seedMark



if __name__ == '__main__':
    global_lst = []
    def get_xy(img):
        def getpos(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # print((x, y), '  ', img[y, x])
                global global_lst
                global_lst.append([x,y])
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.imshow('img', img)
        cv2.setMouseCallback('img', getpos)
        cv2.waitKey(0)

    img = cv2.imread('./image/watershed.jpg', 0)
    # hist = cv2.calcHist([img], [0], None, [256], [0,256])  # 计算直方图 选择合适阈值
    # plt.plot(hist)
    # plt.show()
    # seeds = [[75, 50], [100, 180]]
    get_xy(img)
    binaryImg = regionGrow(img, global_lst, 10)
    cv2.imshow('ret', binaryImg)
    cv2.waitKey(0)
