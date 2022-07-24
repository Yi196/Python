import numpy as np
import cv2
import matplotlib.pyplot as plt


'''
先把图像分成4块
若这其中的一块符合分裂条件，那么这一块又分裂成4块
分裂到一定数量时，以每块为中心，检查相邻的各块，满足一定条件，就合并。
如此循环往复进行分裂和合并的操作。
最后合并小区，即把一些小块图像的合并到旁边的大块里。
'''

# 判断方框是否需要再次拆分为四个
def judge(img, img_split, w0, h0, w, h, min_area, std_th):
    temp = img[h0: h0 + h, w0: w0 + w]
    ave = np.mean(temp)
    std = np.std(temp)
    min_val, max_val, _, _ = cv2.minMaxLoc(temp)
    # print(std)
    if std < std_th or min(w, h) <= min_area:
        # if max_val - min_val > thresh:
        img_split[h0: h0 + h, w0: w0 + w] = ave
        return False
    else:
        return True



def function(img, img_split, w0, h0, w, h, min_area, std, img_draw, show_pic):
    '''
        img: 输入图像
        img_split: 输出图像
        w0, h0, w, h: 目标区域的左上角坐标和区域宽、长
        min_area: 分裂区域的最小边长
        std: 均方差阈值 （均方差小于阈值的区域不再细分）
        img_draw: 用于显示图像分裂过程的图片
        show_pic: 为True时显示分裂过程
    '''
    # 画矩形框
    if show_pic:
        cv2.line(img_draw, (w0, h0 + int(h / 2)), (w0+w, h0 + int(h / 2)), (0, 0, 255), thickness=1)
        cv2.line( img_draw, (w0 + int(w / 2), h0), (w0 + int(w / 2), h0+h), (0, 0, 255), thickness=1)
        cv2.namedWindow('img_split',0)
        cv2.namedWindow('img_draw',0)
        cv2.imshow('img_split', img_split)
        cv2.imshow('img_draw', img_draw)
        cv2.waitKey(5)

    if judge(img, img_split, w0, h0, w, h, min_area, std):
        function(img, img_split, w0, h0, int(w / 2), int(h / 2), min_area, std, img_draw, show_pic)
        function(img, img_split, w0 + int(w / 2), h0, w - int(w / 2), int(h / 2), min_area, std, img_draw, show_pic)
        function(img, img_split, w0, h0 + int(h / 2), int(w / 2), h - int(h / 2), min_area, std, img_draw, show_pic)
        function(img, img_split, w0 + int(w / 2), h0 + int(h / 2), w - int(w / 2), h - int(h / 2), min_area, std, img_draw, show_pic)



def regionSpilt(img, min_area=3, std=10, show_pic=True):
    '''
        img: 输入图像
        min_area: 分裂区域的最小边长
        std: 均方差阈值 （均方差小于阈值的区域不再细分）
        show_pic: 为True时显示分裂过程
    '''
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_draw = img if show_pic else None
        else:
            gray = img[:, :, 0]
            img_draw = cv2.merge([img] * 3) if show_pic else None
    else:
        gray = img
        img_draw = cv2.merge([img] * 3) if show_pic else None

    img_split = np.zeros_like(gray)
    height, width = gray.shape
    function(gray, img_split, 0, 0, width, height, min_area, std, img_draw, show_pic)
    cv2.destroyAllWindows()
    return img_split

if __name__ == '__main__':
    img = cv2.imread('./image/template_contours.jpg', 0)

    img_split = regionSpilt(img)

    cv2.imshow('input', img)
    cv2.imshow('output', img_split)

    cv2.waitKey()
    cv2.destroyAllWindows()
