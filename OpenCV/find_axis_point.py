import cv2
import numpy as np
import traceback

def find_axis_point(img,rect,axis):
    try:
        ret_dict ={
            '0':0,
            '1':None,
        }
        _, rect_x, rect_y, rect_w, rect_h = [int(i) for i in rect[0][0][:5]]
        img = img[0][rect_y:(rect_y+rect_h),rect_x:(rect_x+rect_w),:]


        w, h = img.shape[:2]
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            pass
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)

        s = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, s)

        binary[0:10, :] = 255
        binary[w - 10:, :] = 255
        binary[:, 0:10] = 255
        binary[:, h - 10:] = 255

        binary = cv2.bitwise_not(binary)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(img,contours,-1,(0,0,255),3)

        #找面积最大轮廓的外接矩形
        a = np.array(list(map(lambda x: cv2.contourArea(x), contours))).argmax()
        x,y,w,h = cv2.boundingRect(contours[a])

        # for bbox in bounding_boxes:
        #     [x, y, w, h] = bbox
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)

        # cv2.imshow('img', binary)
        # cv2.waitKey()

        x = x + rect[0][0][1]
        y = y + rect[0][0][2]

        if axis=='DOWN' or axis=='RIGHT':
            ret_dict['1'] = [[[4.0,x+w,y+h]]]
        else:
            ret_dict['1'] = [[[4.0,x , y]]]

        return ret_dict

    except Exception as e:
        traceback.print_exc()
        ret_dict = {
            "0": -1,
            "1": None,
        }
        return ret_dict
