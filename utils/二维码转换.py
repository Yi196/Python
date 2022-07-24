import cv2
import numpy as np


# 返回左上右下角坐标
def _find_rect(img):
    h, w = img.shape
    x_left = w//2
    y_left = h//2
    x_right = 0
    y_right = 0
    for i in range(h):
        for j in range(w):
            if img[i,j] != 255:
                if i < y_left:
                    y_left = i
                if j < x_left:
                    x_left = j
                if i > y_right:
                    y_right = i
                if j >x_right:
                    x_right = j
    return [x_left,y_left,x_right,y_right]

# 计算每个方格内像素占比
def _calculate(part):
    h, w = part.shape
    sum = 0
    for i in range(h):
        for j in range(w):
            if part[i,j] != 255:
                sum += 1
    return sum / (h*w)



def main(img):
    img_show = img.copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray,9,75,75)

    _, binary = cv2.threshold(blur, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    points = _find_rect(binary)
    point_left = [points[0],points[1]]
    point_right = [points[2],points[3]]
    long_x = abs(point_left[0] - point_right[0]) / 22
    long_y = abs(point_left[1] - point_right[1]) / 22
    # print(long_x,long_y)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    img_d = cv2.dilate(binary, kernel,iterations=1)

    ret = np.ones((22,22),)
    for i in range(22):
        for j in range(22):
            part = img_d[int(point_left[1] + i*long_y):int(point_left[1] + (i+1)*long_y),
                   int(point_left[0] + j*long_x):int(point_left[0] + (j+1)*long_x)]
            score = _calculate(part)
            if score > 0.3:
                ret[i,j] = 0
                cv2.circle(img_show,(int((point_left[0] + j*long_x+point_left[0] + (j+1)*long_x)/2),
                                     int((point_left[1] + i*long_y+point_left[1] + (i+1)*long_y)/2)),2,(0,0,255),-1)
            # 显示
            # if 0.2 < score < 0.4:
            #     print(score)
            #     cv2.imshow('', part)
            #     cv2.waitKey(0)
            #     img_temp = img_d[int(point_left[1] + (i-1)*long_y):int(point_left[1] + (i+2)*long_y),
            #        int(point_left[0] + j*long_x):int(point_left[0] + (j+1)*long_x)]
            #     cv2.line(img_temp,(0,int(long_y)),(int(long_x),int(long_y)),(0,0,255),1)
            #     cv2.line(img_temp,(0,int(2*long_y)),(int(long_x),int(2* long_y)),(0,0,255),1)
            #     cv2.imshow('', img_temp)
            #     cv2.waitKey(0)

    return ret, img_show

if __name__ == '__main__':
    import os
    # img = cv2.imread(r'../temp/001.jpeg')
    dir = r'../../temp/2'
    for name in os.listdir(dir):
        img = cv2.imread(os.path.join(dir,name))
        ret,img_show = main(img)
        print(ret)
        cv2.imshow('',img_show)
        cv2.waitKey(0)