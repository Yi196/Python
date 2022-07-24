import cv2, _pickle, time
import numpy as np
import os

class Matching(object):
    def __init__(self):
        self.threshold = 110
        # 只匹配中心附近的点
        self.x_m = [85, 115]
        self.y_m = [120, 160]
        self.min_score = 0.95 # 匹配点数满足时才算匹配成功

        # 载入模板
        self.file_path = r'./template/template.pkl'
        template = self._read_template()
        self.number_point = template['points_number']
        self.points_temp = template['points']
        self.m_min = int((1-self.min_score) * self.number_point)
        self.count_min = int(self.min_score * self.number_point)

        # 检测黄胶带
        self.lowerb = np.array([26,11,46])
        self.upperb = np.array([41,255,255])
        # 掩去周围区域
        self.mask_y = [50,225]
        self.mask_x = [25,170]

    def detect(self,img):
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_hsv = cv2.cvtColor(img[self.mask_y[0]:self.mask_y[1],self.mask_x[0]:self.mask_x[1],:], cv2.COLOR_BGR2HSV)
        _, binary = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow('', np.hstack([img,np.stack([binary,binary,binary],-1)]))
        cv2.waitKey(0)
        # mask = cv2.Canny(gray,60,90)
        # cv2.imshow('', mask)
        # cv2.waitKey(0)
        _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        def _cont_area(cont):
            return cv2.contourArea(cont)
        contours.sort(key=_cont_area, reverse=True)
        points = contours[1]   # [[[x1,y1]],[[x2,y2]],...]
        points = np.squeeze(points, 1)  # # [[x1,y1],[x2,y2],...]
        mask = np.zeros_like(binary)
        for x, y in points:
            mask[y-2:y+2, x-2:x+2] = 255

        # cimg = np.zeros_like(img)
        # cimg[:, :, :] = 255
        # cv2.drawContours(cimg, contours, 1, color=(0, 0, 0), thickness=-1)
        # img_t = cv2.bitwise_or(img, cimg)
        # img_hsv = cv2.cvtColor(img_t,cv2.COLOR_BGR2HSV)
        # cv2.imshow('',mask)
        # cv2.waitKey(0)

        for i in range(self.y_m[0], self.y_m[1]):
            for j in range(self.x_m[0], self.x_m[1]):
                count = 0
                result_points = []
                for m in range(self.number_point):
                    # 计算对应点坐标
                    x_matchimg = j + self.points_temp[m][0]
                    y_matchimg = i + self.points_temp[m][1]

                    if y_matchimg<0 or x_matchimg<0 or y_matchimg > h-1 or x_matchimg > w-1:
                        continue

                    if mask[y_matchimg, x_matchimg] == 255:
                        count += 1

                    if not (count > m-self.m_min):
                        break


                if count > self.count_min:
                    # result_points.append([j, i])
                    return self._detect_huangjiaodai(img_hsv,img)


                    # 显示匹配到的对象
                    # print(count,result_points)
                    # img_show = img.copy()
                    # for x, y in result_points:
                    #     for i, j in points_temp:
                    #         cv2.circle(img_show, (int(i + x), int(j + y)), 1, (0, 0, 255), -1)
                    # cv2.imshow('', img_show)
                    # cv2.waitKey(0)

                    # return result_points

        else:
            # cv2.imshow('', np.hstack([img,np.stack([binary,binary,binary],-1)]))
            # cv2.waitKey(0)
            return 'kongliao'


    def _read_template(self):
        with open(self.file_path,'rb') as file:
            template = _pickle.load(file)
        return template

    def _detect_huangjiaodai(self,img_hsv,img):
        mask = cv2.inRange(img_hsv,self.lowerb,self.upperb)
        if len(mask[mask==255]) > 500:
            # print(len(mask[mask==255]))
            # cv2.imshow('',img)
            # cv2.waitKey(0)
            return 'huangjiaodai'
        else:
            # print(len(mask[mask == 255]))
            # cv2.imshow('', img)
            # cv2.waitKey(0)
            return 'liangpin'


if __name__ == '__main__':
    from tqdm import tqdm
    dir_img = r'../../000'
    matching = Matching()
    count_l = 0
    count_k = 0
    count_h = 0
    for name in tqdm(os.listdir(dir_img)):
        img = cv2.imread(os.path.join(dir_img,name))
        ret = matching.detect(img)
        if ret == 'liangpin':
            count_l += 1
        elif ret == 'kongliao':
            count_k += 1
        elif ret == 'huangjiaodai':
            count_h += 1
    print('良品：',count_l,'\n','空料：',count_k,'\n','黄胶带：',count_h)