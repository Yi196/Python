import os
import cv2
import numpy as np
from OpenCV.detect_first_line import detect_line_subpixel

class Detect_paomian(object):
    def __init__(self):
        pass

    def detect(self,img):
        # _, mask = cv2.threshold(img,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        mask = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)
        # img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #
        # lower_red = np.array([81, 71, 85])
        # upper_red = np.array([255, 164, 251])
        # mask = cv2.inRange(img_hsv, lower_red, upper_red)
        #
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (6, 6))
        # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # cv2.namedWindow('img_hsv', 0)
        # cv2.resizeWindow('img_hsv', 600, 380)
        # cv2.imshow('img_hsv', mask)
        # cv2.waitKey(0)

        # get_xy(mask)

        detect_line_rect = [[362, 225,561, 295],[357, 164,576, 213],[54, 260,216, 320],
                            [423, 527,508, 844],[590, 537,667, 817],[1852, 780,1998, 845]]
        detect_orient = ['从上到下','从下到上','从下到上','从右到左','从左到右','从下到上']
        detect_brightness = ['从白到黑','从白到黑','从白到黑','从白到黑','从白到黑','从白到黑']
        for rect, orient,brightness in zip(detect_line_rect,detect_orient,detect_brightness):
            line, coeff, _, angle = detect_line_subpixel(mask,rect,orient,brightness,mag_thresh=90)
            if coeff is not None:
                if 3 < abs(angle) < 87:
                    mask = np.stack([mask,mask,mask],axis=-1)
                    cv2.rectangle(mask,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
                    x0, y0, x1, y1 = line
                    cv2.line(mask, (int(x0), int(y0)), (int(x1), int(y1)), (0, 0, 255),4)
                    cv2.namedWindow('img_hsv', 0)
                    cv2.resizeWindow('img_hsv', 600, 380)
                    cv2.imshow('img_hsv', mask)
                    cv2.waitKey(0)
                    return False
            else:
                return False
        else:
            # cv2.namedWindow('img_hsv', 0)
            # cv2.resizeWindow('img_hsv', 600, 380)
            # cv2.imshow('img_hsv', mask)
            # cv2.waitKey(0)
            return True





if __name__ == '__main__':

    import time

    start = time.time()
    detect_paomian = Detect_paomian()

    names = [r'../OpenCV/image/008.png',]
    num_true = 0
    num_false = 0
    for name in names:
        img = cv2.imread(name)
        ret = detect_paomian.detect(img)
        if ret:
            num_true += 1
        else:
            num_false += 1
    print('True:',num_true,'\n','False:',num_false)
    print('Time:',time.time()-start)