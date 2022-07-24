import traceback
import cv2
import matplotlib.pyplot as plt
import numpy as np
# import fs
import os
import pandas as pd
from PIL import Image, ImageEnhance

"""
Anchor Finder

"""


def agg_dims(img, posn, rng, direct):
    if direct == 'left':
        return img[posn[0], posn[1] - int(rng/2): posn[1] + int(rng/2)].sum()
    elif direct == 'right':
        return img[posn[0], posn[1] - int(rng/2): posn[1] + int(rng/2)].sum()
    elif direct == 'up':
        return img[posn[0] - int(rng/2): posn[0] + int(rng/2), posn[1]].sum()
    else:
        return img[posn[0] - int(rng/2): posn[0] + int(rng/2), posn[1]].sum()


def search_anchor_border(img, direct, init):
    count = 1
    init = (int(init[0]), int(init[1]))
    if direct == "left" or direct == "right":
        if direct == "left":
            init_X = -1
            threshold = 200
        else:
            init_X = 1
            threshold = 200
        while True:
            if init[1] + init_X * count >= img.shape[1] or init[1] + init_X * count < 0:
                break
            if agg_dims(img, (init[0], init[1] + init_X * count), 2, direct) > threshold:
                return init[1] + init_X * count
            count += 1
            if count > 130:
                print(direct)
                raise TimeoutError()
    else:
        if direct == "up":
            init_Y = -1
            threshold = 200
        else:
            init_Y = 1
            threshold = 200
        while True:
            if init[0] + init_Y * count >= img.shape[0] or init[0] + init_Y * count < 0:
                break
            if agg_dims(img, (init[0] + init_Y * count, init[1]), 2, direct) > threshold:
                return init[0] + init_Y * count
            count += 1
            if count > 130:
                print(direct)
                raise TimeoutError()
    raise TimeoutError()


def get_grad(img):
    img = cv2.bilateralFilter(img, 7, 75, 75)
    grad_x = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    grad_y = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    gradx = cv2.convertScaleAbs(grad_x)
    grady = cv2.convertScaleAbs(grad_y)
    img = cv2.addWeighted(gradx, 0.5, grady, 0.5, 0)

    return img


def get_anchor(img, rect):
    try:
        ret_dict = {
            '0': 0,
            '1': None,
        }
        # img_1 = img.copy()
        _, rect_x, rect_y, rect_w, rect_h = [int(i) for i in rect[0][0][:5]]
        img = img[0][rect_y:(rect_y + rect_h), rect_x:(rect_x + rect_w), :]

        if len(img.shape) > 2:
            if img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                img = img[:, :, 0]
        else:
            img = img

        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.Canny(img, 70, 30)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # img = clahe.apply(img)
        #
        # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 7)
        #
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        # cv2.imshow('', img)
        # cv2.waitKey()

        point_y = int(img.shape[0] / 2)
        point_x = int(img.shape[1] / 2)
        init = [point_y, point_x]

        for _ in range(6):
            # horizontal scan
            left_b = search_anchor_border(img, "left", init)
            right_b = search_anchor_border(img, "right", init)
            init[1] = (left_b + right_b) / 2

            # vertical scan
            upper_b = search_anchor_border(img, "up", init)
            lower_b = search_anchor_border(img, "low", init)
            init[0] = (upper_b + lower_b) / 2
        y = init[0] + rect_y
        x = init[1] + rect_x
        ret_dict['1'] = [[[4.0,x, y],[4.0, abs(left_b - right_b) / 2, abs(upper_b - lower_b) / 2]]]
        # cv2.circle(img_1[0], (int(x),int(y)),  int(abs(left_b - right_b) / 2), (0, 0, 255), 1 )
        return ret_dict
    except Exception as e:
        traceback.print_exc()
        ret_dict = {
            "0": -1,
            "1": [[[-1,-1,-1],[-1,-1,-1]]],
        }
        return ret_dict

if __name__ == '__main__':
    path = r'C:\Users\dihuge\Desktop\342\003.png'
    img = cv2.imread(path)
    ret_dict = get_anchor([img],rect=[[[4.0,0,0,160,180]]])
    print(ret_dict)