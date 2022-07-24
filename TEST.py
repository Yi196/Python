import cv2
import numpy as np


def filter(labels, rects, confidents, filter_label:int, pixel_x:int):
    ret_dict = {
        '0': 0,
        '1': 'Success',
        '2': None,
        '3': None,
        '4': None,
    }
    try:
        for idx, label in enumerate(labels):
            if filter_label not in label:
                continue
            rect = rects[idx]
            len_label = len(label)
            for idx_filter, label_f in enumerate(label[::-1]):
                if label_f != filter_label:
                    continue
                idx_filter = len_label - idx_filter - 1
                center_x = int(rect[idx_filter][1] + rect[idx_filter][1] + rect[idx_filter][3]) / 2

                if center_x < pixel_x:
                    labels[idx].pop(idx_filter)
                    rects[idx].pop(idx_filter)
                    confidents[idx].pop(idx_filter)



        ret_dict['2'] = labels
        ret_dict['3'] = rects
        ret_dict['4'] = confidents
        return ret_dict

    except Exception as e:
        ret_dict['0'] = -1
        ret_dict['1'] = str(e)
        return ret_dict

