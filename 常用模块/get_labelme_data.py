# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Peng Xu, Bingzhang Hu
# @Email   : bingzhanghu1992@gmail.com
# @File    : get_labelme_data.py
# function : converting labelme annotations to detectron2 annotations
import json
import os

import cv2
import numpy as np
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.structures import BoxMode
from detectron2.utils.visualizer import Visualizer



def labelme2dicts_seg(jsonname, imgdir, image_id):
    label = json.load(open(jsonname, 'r'))
    data_dict = {}
    file_name = os.path.join(imgdir, label['imagePath'])
    height = label['imageHeight']
    width = label['imageWidth']
    annos = label["shapes"]
    objs = []
    for anno in annos:
        px = [a[0] for a in anno['points']]
        py = [a[1] for a in anno['points']]
        poly = [(x, y) for x, y in zip(px, py)]
        poly = [p for x in poly for p in x]
        obj = {
            "bbox": [np.min(px), np.min(py), np.max(px), np.max(py)],
            "bbox_mode": BoxMode.XYXY_ABS,
            "segmentation": [poly],
            "category_id": int(anno['label']),
            "iscrowd": 0
        }
        objs.append(obj)
    data_dict = {
        'file_name': file_name,
        'image_id': image_id,
        'height': height,
        'width': width,
        'annotations': objs,
    }
    return data_dict


def labelme2dicts(jsonname, imgdir, image_id):
    label = json.load(open(jsonname, 'r'))
    data_dict = {}
    file_name = os.path.join(imgdir, label['imagePath'])
    height = label['imageHeight']
    width = label['imageWidth']
    objs = []
    category_id = -1
    for poly in label['shapes']:
        pts = poly['points']
        pts = np.array(pts)
        xmin, xmax = np.min(pts[:, 0]), np.max(pts[:, 0])
        ymin, ymax = np.min(pts[:, 1]), np.max(pts[:, 1])

        # TODO
        if poly['label'] == '0':
            category_id = 0
        elif poly['label'] == '1':
            category_id = 1
        elif poly['label'] == '2':
            category_id = 2
        elif poly['label'] == '3':
            category_id = 3
        elif poly['label'] == '4':
            category_id = 4
        elif poly['label'] == '5':
            category_id = 5
        elif poly['label'] == '6':
            category_id = 6
        elif poly['label'] == '7':
            category_id = 7
        elif poly['label'] == '8':
            category_id = 8
        elif poly['label'] == '9':
            category_id = 9
 

        obj = {
            'bbox': [xmin, ymin, xmax, ymax],
            'bbox_mode': BoxMode.XYXY_ABS,
            # 'category_id': int(poly['label']),
            'category_id': category_id,
            'iscrowd': 0,
        }
        objs.append(obj)
    data_dict = {
        'file_name': file_name,
        'image_id': image_id,
        'height': height,
        'width': width,
        'annotations': objs,
    }
    return data_dict


def get_data_dicts(indir):
    data_dicts = []
    existing_label = {}
    statistics = {}
    num_existing_label = 0
    imgdir = os.path.join(indir, 'images')
    jsondir = os.path.join(indir, 'jsons')
    image_id = 0
    for name in os.listdir(imgdir):
        imgname = os.path.join(imgdir, name)
        jsonname = os.path.join(jsondir, name[:-4] + '.json')
        # print(imgname)
        img = cv2.imread(imgname)
        print(imgname)
        h, w = img.shape[:2]
        if not os.path.isfile(jsonname):
            # print(name)
            data_dict = {
                'image_id': image_id,
                'file_name': imgname,
                'height': h,
                'width': w,
                'annotations': [],
            }
            image_id += 1
        else:
            data_dict = labelme2dicts(jsonname, imgdir, image_id)
            # data_dict = labelme2dicts_seg(jsonname, imgdir, image_id)
            image_id += 1
            # split to n function may cause empty label in json file
            if len(data_dict['annotations']) > 0:
                for i, obj in enumerate(data_dict['annotations']):
                    if num_existing_label == 0:
                        existing_label[obj['category_id']] = num_existing_label
                        # data_dict['annotations'][i]['category_id'] = num_existing_label
                        statistics[num_existing_label] = 1
                        num_existing_label += 1
                    elif not obj['category_id'] in existing_label.keys():
                        existing_label[obj['category_id']] = num_existing_label
                        # data_dict['annotations'][i]['category_id'] = num_existing_label
                        statistics[num_existing_label] = 1
                        num_existing_label += 1
                    else:
                        for (key, value) in existing_label.items():
                            if obj['category_id'] == key:
                                # data_dict['annotations'][i]['category_id'] = value
                                statistics[value] += 1
        data_dicts.append(data_dict)
    # print('标签映射:')
    # for (key, value) in existing_label.items():
    #     print('%s -> %d' % (defect[key], value))
    # print('统计:')
    # for (key, value) in statistics.items():
    #     detect_name = defect[list(existing_label.keys())[list(existing_label.values()).index(key)]]
    #     print('%s : %d' % (detect_name, value))
    return data_dicts


# TODO
# def get_statistics(data_dicts):
#     pass

def show_img(indir):
    data_dicts = get_data_dicts(indir)
    tl_metadata = MetadataCatalog.get(indir)
    for data_dict in data_dicts:
        imgname = data_dict['file_name']
        img = cv2.imread(imgname)
        visualizer = Visualizer(img[:, :, ::-1], metadata=tl_metadata, scale=1)
        vis = visualizer.draw_dataset_dict(data_dict)
        cv2.imshow('visual', vis.get_image()[:, :, ::-1])
        cv2.waitKey(0)


def regist_dataset(indir, name):
    print(name)
    DatasetCatalog.register(name, lambda: get_data_dicts(indir))
    # metadata = MetadataCatalog.get(name + d)
    # dataset_dicts = DatasetCatalog.get(name+d)
    # for dic in random.sample(dataset_dicts, 30):
    #     img = cv2.imread(dic["file_name"])
    #     visualizer = Visualizer(img[:, :, ::-1], metadata=metadata, scale=0.5)
    #     vis = visualizer.draw_dataset_dict(dic)
    #     cv2.imshow(d, vis.get_image()[:, :, ::-1])
    #     cv2.waitKey()
    #     cv2.destroyAllWindows()
