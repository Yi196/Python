import cv2
import numpy as np
# from configs.config import DEFECTS
import time
import os

# 计算Y方向边数量
class Detect_Yiwei(object):
    def __init__(self):
        self.dist_ignore = 5

    def get_lianxu_true(self,the_sum):
        l = []
        ll = []
        for i in range(the_sum.size):
            if the_sum[i] == True:
                ll.append(i)
                # print("ll:",ll)
            else:
                if len(ll) > 0:
                    l.append(ll)
                    ll = []
        if len(ll) != 0:
            l.append(ll)

        # 忽略较小位移
        del_lst = []
        for i in range(len(l) - 1):
            if l[i+1][0]-l[i][-1] < self.dist_ignore + 1:
                del_lst.append(i)
        for i in del_lst[::-1]:
            l.pop(i)
        return len(l)


    def detect(self,src):
        ret_dict = {
            'vaild': True,
            'defect': 0,    # DEFECTS.LIANGPIN
            'image': src,
        }

        img = src.copy()
        img = img[:,:,0]
        img = cv2.bilateralFilter(img, 3, 75, 75)
        binary = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,3)
        kernel = np.ones((1,3),np.uint8)
        binary = cv2.erode(binary,kernel,iterations=4)


        cv2.imshow('', binary)
        cv2.waitKey(0)

        sum_binary = np.sum(binary, axis=1)

        the_sum = sum_binary > int(15 * 255)  # 大于15个像素被视为线
        # print("the_sun:",the_sum)

        num_lines = self.get_lianxu_true(the_sum)
        # print('num_lines', num_lines)

        if num_lines == 2:
            return ret_dict
        else:
            ret_dict['defect'] = 1  # DEFECTS.PIANXIN
            return ret_dict




if __name__ == '__main__':
    yiwie = Detect_Yiwei()
    img = cv2.imread(r'../OpenCV/image/010.png')
    print(yiwie.detect(img))