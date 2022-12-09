import os
import time
import uuid
import cv2
import numpy as np
import json
import xml.etree.ElementTree as ET


def labelimg2codeX_xml(xml_dir):
    '''
    labelimg 标注的voc数据格式为xml文件
    :param xml_dir: xml文件夹
    :return:
    '''

    file_names = os.listdir(xml_dir)
    save_dir = os.path.join(xml_dir, 'codeX_json')
    os.makedirs(save_dir, exist_ok=True)

    for file in file_names:
        name, suffix = os.path.splitext(file)
        if suffix != '.xml':
            continue
        tree = ET.parse(os.path.join(xml_dir, file))
        root = tree.getroot()

        temp_rect = {"label_box2D": []}
        num_rectangle = 1
        for ob in root.iter('object'):
            for t in ob.iter('name'):
                category = t.text
            rect = []
            for bndbox in ob.iter('bndbox'):
                for l in bndbox:
                    rect.append(l.text)

            temp = {"number": str(num_rectangle), "instanceId": str(uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))),
                    "box2D": {"xmin": str(rect[0]), "ymin": str(rect[1]), "xmax": str(rect[2]), "ymax": str(rect[3])},
                    "attributes": {}, "category": str(category)}
            temp_rect['label_box2D'].append(temp)
            num_rectangle += 1
        # print(temp_rect)

        temp_dir = os.path.join(save_dir, 'rectangle')
        os.makedirs(temp_dir, exist_ok=True)
        save_json_path = os.path.join(temp_dir, name + '.json')
        with open(save_json_path, 'w') as f:
            f.write(json.dumps(temp_rect))


def labelimg2codeX_txt(txt_dir):
    '''
    labelimg 标注的coco数据格式为txt文件
    每一行代表标注的一个目标
    第一个数代表标注目标的标签，第一目标circle_red，对应数字就是0
    后面的四个数代表标注框的中心坐标和标注框的相对宽和高
    会生成一个classes.txt记录标签名称
    :param txt_dir: txt文件夹
    :return:
    '''
    file_names = os.listdir(txt_dir)
    save_dir = os.path.join(txt_dir, 'codeX_json')
    os.makedirs(save_dir, exist_ok=True)

    img_names = [i for i in file_names if os.path.splitext(i)[1] != '.txt']
    img_prefix = [os.path.splitext(i)[0] for i in img_names]

    with open(os.path.join(txt_dir, 'classes.txt'), 'r') as f:
        label_names = [i.strip() for i in f.readlines()]

    for file in file_names:
        name, suffix = os.path.splitext(file)
        if suffix != '.txt' or file == 'classes.txt':
            continue

        with open(os.path.join(txt_dir, file), 'r') as f:
            label_lst = f.readlines()

        img_idx = img_prefix.index(name)
        img_path = os.path.join(txt_dir, img_names[img_idx])
        img = cv2.imread(img_path)
        img_height, img_width = img.shape[:2]

        temp_rect = {"label_box2D": []}
        num_rectangle = 1
        for l in label_lst:
            l = [float(i) for i in l.strip().split(' ')]
            category = label_names[int(l[0])]
            center_x, center_y, width, height = l[1:5]
            xmin = max(round((center_x - width / 2.0) * img_width, 2), 0)
            ymin = max(round((center_y - height / 2.0) * img_height, 2), 0)
            xmax = min(round((center_x + width / 2.0) * img_width, 2), img_width)
            ymax = min(round((center_y + height / 2.0) * img_height, 2), img_height)

            temp = {"number": str(num_rectangle), "instanceId": str(uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))),
                    "box2D": {"xmin": str(xmin), "ymin": str(ymin), "xmax": str(xmax), "ymax": str(ymax)},
                    "attributes": {}, "category": str(category)}
            temp_rect['label_box2D'].append(temp)
            num_rectangle += 1
        # print(temp_rect)

        temp_dir = os.path.join(save_dir, 'rectangle')
        os.makedirs(temp_dir, exist_ok=True)
        save_json_path = os.path.join(temp_dir, name + '.json')
        with open(save_json_path, 'w') as f:
            f.write(json.dumps(temp_rect))


if __name__ == '__main__':
    xml_dir = '/home/mafneg/桌面/labelme/labelimg_txt'

    for i in os.listdir(xml_dir):
        suffix = os.path.splitext(i)[1]
        if suffix == '.xml':
            labelimg2codeX_xml(xml_dir)
            break
        elif suffix == '.txt':
            labelimg2codeX_txt(xml_dir)
            break