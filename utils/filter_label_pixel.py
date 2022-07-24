import cv2
import numpy as np


def filter(imgs, rects, labels, filter_label:int, thresh_b, thresh_num, is_component=False, width=None, height=None):
    ret_dict = {
        '0': 0,
        '1': 'Success',
        '2': None,
        '3': None,
        '4': None,
        '5': None,
        '6': None,
    }
    try:
        count_lst = []
        binary_lst = []
        w_h_lst = []
        for idx, label in enumerate(labels):
            if filter_label not in label:
                continue
            rect = rects[idx]
            img = imgs[idx]
            len_label = len(label)
            for idx_filter, label_f in enumerate(label[::-1]):
                if label_f != filter_label:
                    continue
                idx_filter = len_label - idx_filter - 1
                scr = img[int(rect[idx_filter][2]):int((rect[idx_filter][2] + rect[idx_filter][4])),
                      int(rect[idx_filter][1]):int((rect[idx_filter][1] + rect[idx_filter][3])), :]
                scr = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(scr, thresh_b, 255, cv2.THRESH_BINARY_INV)
                count = cv2.countNonZero(binary)
                binary_lst.append({'image': binary})
                count_lst.append(count)

                is_c = False
                if is_component:
                    # 計算最大連通域的外接矩形
                    _, _, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8, ltype=None)
                    temp = stats[:, 4].argsort()
                    max_c_idx = temp[-1] if temp[-1] else temp[-2]
                    width_max, height_max = stats[max_c_idx][2:4]
                    w_h_lst.append([width_max, height_max])
                    if width_max < width and height_max < height:
                        is_c = True

                if count < thresh_num:
                    labels[idx].pop(idx_filter)
                    rects[idx].pop(idx_filter)
                else:
                    if is_c:
                        labels[idx].pop(idx_filter)
                        rects[idx].pop(idx_filter)

        ret_dict['2'] = labels
        ret_dict['3'] = rects
        ret_dict['4'] = count_lst
        ret_dict['5'] = binary_lst
        ret_dict['6'] = w_h_lst if w_h_lst != [] else [[]]
        return ret_dict

    except Exception as e:
        ret_dict['0'] = -1
        ret_dict['1'] = str(e)
        return ret_dict

