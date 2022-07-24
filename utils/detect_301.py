import numpy as np
import cv2,os
import traceback,pdb




def detect_301_algorithm(img, threshold):
    img = img[0]
    ret_dict = {
        '0':0,
        '1':'Success',
        '2':[{'image':img}],
        '3':'OK'
    }
    # pdb.set_trace()
    try:
        # 检测红色画线
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        red_low = np.array([160, 100, 51])
        red_high = np.array([255, 255, 255])
        img_red = cv2.inRange(img_hsv, red_low, red_high)
        count_red = cv2.countNonZero(img_red)
        if count_red > 1000:
            # print('count_red', count_red)
            ret_dict['3'] = 'NG'
            return ret_dict


        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_low = np.array([0, 25, 40])
        hsv_high = np.array([83, 255, 255])
        img_t = cv2.inRange(img_hsv, hsv_low, hsv_high)

        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (9, 9))
        img_erode = cv2.erode(img_t, kernel)
        contours, hierarchy = cv2.findContours(img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        def cont_area(cont):
            return cv2.contourArea(cont)

        contours.sort(key=cont_area, reverse=True)
        mask = np.zeros_like(img_erode)
        mask[:, :] = 255
        for i in range(4):
            cv2.drawContours(mask, contours, i, (0, 0, 0), -1)

        # 检测黄色像素数量
        mask_y = cv2.bitwise_not(mask)
        count_y = cv2.countNonZero(mask_y) // 10000
        # if count_y < 174 or count_y > 176:  # 300
        if count_y < 249 or count_y > 262 :    # 301
            # print('count_yellow//10000', count_y)
            ret_dict['3'] = 'NG'
            return ret_dict

        img_ret = cv2.bitwise_or(img_erode, mask)
        img_ret = cv2.bitwise_not(img_ret)
        count = cv2.countNonZero(img_ret)
        # print(count)

        if count > threshold:   # 50
            # print(count)
            # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
            # cv2.imshow('img', img)
            # cv2.namedWindow('ret', cv2.WINDOW_NORMAL)
            # cv2.imshow('ret', img_ret)
            # cv2.waitKey(0)
            ret_dict['3'] = 'NG'
        return ret_dict
    except Exception as e:
        ret_dict['0'] = -1
        ret_dict['1'] = e
        return ret_dict



if __name__ == '__main__':
    path = r'/home/dihuge/data/logs/roi/cam0/'
    names = os.listdir(path)
    for name in names:
        img = cv2.imread(os.path.join(path, name))
        ret = detect_301_algorithm(img, 120)
        # print(ret)