import os
import time
import uuid
import cv2
import numpy as np
import json
from labelme import utils


def labelme2codeX(json_dir):
    '''
    将labelme标注转为开发平台标注格式
    若labelme_json中含有图片信息,会自动提取图片信息
    若labelme_json中含有多种标注类型,会自动区分标注类型
    若labelme_json为空, 会更据前一张图片的类型生成空json
    :param json_dir: labelme标注的json图片地址
    :return:
    '''

    file_names = os.listdir(json_dir)
    save_dir = os.path.join(json_dir, 'codeX_json')
    os.makedirs(save_dir, exist_ok=True)

    type_label = None
    for file in file_names:
        name, suffix = os.path.splitext(file)
        if suffix != '.json':
            continue
        with open(os.path.join(json_dir, file), 'r') as f:
            labelme_json = json.loads(f.read())
        # print(labelme_json)

        # json为空时直接保存
        if not labelme_json:
            if type_label:
                temp_dir = os.path.join(save_dir, type_label[0])
                os.makedirs(temp_dir, exist_ok=True)
                save_json_path = os.path.join(temp_dir, file)
                with open(save_json_path, 'w') as f:
                    f.write(json.dumps(type_label[1]))
            continue

        # 若有图片数据直接保存
        original_img_path = labelme_json.get('imagePath')
        original_img_name = os.path.split(original_img_path)[1]
        if '\\' in original_img_path and len(original_img_path) == len(original_img_name):
            original_img_name = original_img_path.split('\\')[1]

        if labelme_json.get('imageData'):
            img = utils.img_b64_to_arr(labelme_json['imageData'])
            cv2.imwrite(os.path.join(save_dir, original_img_name), img)

        temp_point = {"label_point": []}
        temp_rect = {"label_box2D": []}
        temp_polygon = {"label_polygon": []}
        num_point = 1
        num_rectangle = 1
        num_polygon = 1
        for i in labelme_json['shapes']:
            category = i['label']
            if i['shape_type'] == 'point':
                temp = {"number": str(num_point), "instanceId": str(uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))),
                        "point": {"x": str(round(i['points'][0][0], 2)), "y": str(round(i['points'][0][1], 2))},
                        "attributes": {}, "category": str(category)}
                temp_point['label_point'].append(temp)
                num_point += 1

            elif i['shape_type'] == 'rectangle':
                if i['points'][0][0] < i['points'][1][0]:
                    rect = [[round(i[0], 2), round(i[1], 2)] for i in i['points']]
                else:
                    rect = [[round(i[0], 2), round(i[1], 2)] for i in i['points'][::-1]]

                temp = {"number": str(num_rectangle), "instanceId": str(uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))),
                        "box2D": {"xmin": str(rect[0][0]), "ymin": str(rect[0][1]), "xmax": str(rect[1][0]), "ymax": str(rect[1][1])},
                        "attributes": {}, "category": str(category)}
                temp_rect['label_box2D'].append(temp)
                num_rectangle += 1

            elif i['shape_type'] == 'polygon':
                point_lst = []
                for p in i['points']:
                    point_lst.append({'x': str(round(p[0], 2)), 'y': str(round(p[1], 2))})

                temp = {"number": str(num_polygon), "instanceId": str(uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))),
                        "polygon": {"top": {}, "bottom": point_lst}, "attributes": {}, "category": str(category)}
                temp_polygon['label_polygon'].append(temp)
                num_polygon += 1

        # 保存
        if temp_point['label_point']:
            type_label = ['point', {"label_point": []}]
            temp_dir = os.path.join(save_dir, 'point')
            os.makedirs(temp_dir, exist_ok=True)
            save_json_path = os.path.join(temp_dir, file)
            with open(save_json_path, 'w') as f:
                f.write(json.dumps(temp_point))

        if temp_rect['label_box2D']:
            type_label = ['rectangle', {"label_box2D": []}]
            temp_dir = os.path.join(save_dir, 'rectangle')
            os.makedirs(temp_dir, exist_ok=True)
            save_json_path = os.path.join(temp_dir, file)
            with open(save_json_path, 'w') as f:
                f.write(json.dumps(temp_rect))

        if temp_polygon['label_polygon']:
            type_label = ['polygon', {"label_polygon": []}]
            temp_dir = os.path.join(save_dir, 'polygon')
            os.makedirs(temp_dir, exist_ok=True)
            save_json_path = os.path.join(temp_dir, file)
            with open(save_json_path, 'w') as f:
                f.write(json.dumps(temp_polygon))


if __name__ == '__main__':
    json_dir = '/home/mafneg/桌面/labelme'
    labelme2codeX(json_dir)