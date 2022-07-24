import os, time
import cv2
import numpy as np
# from configs.config import DEFECTS



class Detect_Pianxin(object):
    def __init__(self):
        # Y方向边宽度
        self.line_l_min = 15
        self.line_l_max = 24
        self.line_r_min = 15
        self.line_r_max = 24

    def num_lines(self,binary,num_line,num_ignore,is_X=True,ret_line_num=False):
        '''
        binary: 处理后的二值化图像
        num_line: 像素大于一定数量才被视为线
        num_ignore: 当两条线间距小于num_ignore个像素时 被视为一条线
        is_X: 计算X方向
        '''
        sum_binary = np.sum(binary, axis=1 if is_X else 0)
        the_sum = sum_binary > num_line * 255
        # 判断直线连续
        l = []
        ll = []
        for i in range(len(the_sum)):
            if the_sum[i] == True:
                ll.append(i)
            else:
                if len(ll) > 0:
                    l.append(ll)
                    ll = []
        if len(ll) != 0:
            l.append(ll)

        # 判读两直线间是否较近
        del_lst = []
        for i in range(len(l) - 1):
            if l[i+1][0]-l[i][-1] < num_ignore + 1:
                del_lst.append(i)

        # 将相距较近的线合并为一条直线
        for i in del_lst[::-1]:
            l_i_1 = l[i + 1]
            l_i = l[i]
            l.pop(i + 1)
            l.pop(i)
            l.insert(i, [i for i in range(l_i[0], l_i_1[-1] + 1)])

        # 返回X/Y方向直线 数量
        if ret_line_num:
            return len(l)

        centers = [sum(i)/len(i) for i in l]
        # 返回每条线 中 坐标(X方向直线为Y坐标)
        return centers

    def detect(self, img,show_debug=False):
        ret_dict = {
            'vaild': True,
            'defect': 'liangpin',  # DEFECTS.LIANGPIN,
            'image': None,
        }
        if show_debug:
            ret_dict['image'] = img.copy()

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary_1 = cv2.adaptiveThreshold(img_gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,blockSize=27,C=9)
        # cv2.imshow('', binary_1)
        # cv2.waitKey(0)
        centers_1 = self.num_lines(binary_1, 20, 5, False)
        line_nei_l, line_nei_r = centers_1[0], centers_1[-1]

        out = img_gray * 3
        out[out>255] = 255
        out.astype(np.uint8)
        grad_y = cv2.Sobel(out, cv2.CV_32F, 1, 0)
        grad_y = grad_y * 3
        grady = cv2.convertScaleAbs(grad_y)
        _, binary = cv2.threshold(grady,35,255,cv2.THRESH_BINARY)
        kernel = np.ones((9,1),np.uint8)
        binary = cv2.erode(binary,kernel,iterations=4)
        centers_2 = self.num_lines(binary, 20, 5, False)
        line_wai_l, line_wai_r = centers_2[0], centers_2[-1]

        # cv2.imshow('',binary)
        # cv2.waitKey(0)

        wideth_l = line_nei_l - line_wai_l
        wideth_r = line_wai_r - line_nei_r
        # print(wideth_l,wideth_r)
        if (wideth_l>self.line_l_max and wideth_r<self.line_r_min) or (wideth_l<self.line_l_min and wideth_r>self.line_r_max):
            # print(wideth_l, wideth_r)
            # cv2.imshow('', binary)
            # cv2.waitKey(0)
            ret_dict['defect'] = 'pianxin'    # DEFECTS.PIANXIN
            return ret_dict
        else:
            ret = self._detect_X(img_gray)
            if ret:
                return ret_dict
            else:
                ret_dict['defect'] = 'pianxin'  # DEFECTS.PIANXIN
                return ret_dict
        


    def _detect_X(self,img_gray):
        img = img_gray[90:190, 62:134]
        img = cv2.bilateralFilter(img, 3, 75, 75)
        binary = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
        kernel = np.ones((1, 3), np.uint8)
        binary = cv2.erode(binary, kernel, iterations=4)

        # cv2.imshow('', binary)
        # cv2.waitKey(0)

        num_lines = self.num_lines(binary,15,5,True,True)
        # print('num_lines', num_lines)

        if num_lines >= 3:
            return False
        else:
            return True

if __name__ == '__main__':
    dir = r'../huangjiaodai_1'
    names = os.listdir(dir)
    detect_px = Detect_Pianxin()
    count = 0
    for name in names:
        img = cv2.imread(os.path.join(dir,name))
        ret = detect_px.detect(img)
        if ret==False:
            count += 1
    print(count)

