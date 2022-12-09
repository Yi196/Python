# # -*- coding: utf-8 -*-
import re
import os
import cv2
import time
import json
import uuid
import shutil
import random
import numpy as np
import _pickle as pkl
import math
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import global_variable as globalv


globalv._init()
是 = True
否 = False

SKELETON = [[1, 3], [1, 0], [2, 4], [2, 0], [0, 5], [0, 6], [5, 7], [7, 9], [6, 8],
            [8, 10], [5, 11], [6, 12], [11, 12], [11, 13], [13, 15], [12, 14], [14, 16]]


def get_color(label_names):
    color = [[0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0], [0, 0, 128],
             [128, 0, 128], [0, 128, 128], [128, 128, 128], [64, 0, 0],
             [192, 0, 0], [64, 128, 0], [192, 128, 0], [64, 0, 128],
             [192, 0, 128], [64, 128, 128], [192, 128, 128], [0, 64, 0],
             [128, 64, 0], [0, 192, 0], [128, 192, 0], [0, 64, 128]]
    num_classes = len(label_names)
    if num_classes < 22:
        return color[:num_classes]
    else:
        color = [[random.randint(0, 255) for _ in range(3)] for _ in range(num_classes)]
        color[0] = [0, 0, 0]
        return color


def show_object_detection(img, json_ret, label_names, colors, category=None, threshold=0.25):
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    for i in json_ret:
        if i[5] > threshold:
            if category and label_names[i[0]] != category:
                continue
            box = [i[1], i[2], i[3], i[4]]
            label = f'{label_names[int(i[0])]} {i[5]:.2f}'
            draw.rectangle(box, width=3, outline=tuple(colors[i[0]]))  # plot
            fontsize = max(round(max(img.size) / 40), 12)
            font = ImageFont.truetype(r"./tools/SimHei.ttf", fontsize)
            _, _, txt_width, txt_height = font.getbbox(label)
            draw.rectangle([box[0], box[1] - txt_height, box[0] + txt_width + 1, box[1]], fill=tuple(colors[i[0]]))
            draw.text((box[0] + 1, box[1] - txt_height + 1), label, fill=(255, 255, 255), font=font)

    return np.asarray(img)


def show_human_pose(img, kpt, colors, threshold=0.1):
    for i in range(len(SKELETON)):
        kpt_a, kpt_b = SKELETON[i][0], SKELETON[i][1]
        if kpt[kpt_a][2] > threshold:
            x_a, y_a = kpt[kpt_a][0], kpt[kpt_a][1]
            cv2.circle(img, (int(x_a), int(y_a)), 6, colors[i], -1)
        if kpt[kpt_b][2] > threshold:
            x_b, y_b = kpt[kpt_b][0], kpt[kpt_b][1]
            cv2.circle(img, (int(x_b), int(y_b)), 6, colors[i], -1)
        if kpt[kpt_a][2] > threshold and kpt[kpt_b][2] > threshold:
            cv2.line(img, (int(x_a), int(y_a)), (int(x_b), int(y_b)), colors[i], 2)


def 裁切图像(img_path, rect=None):
    '''
    若要更改传入下个节点的图片（比如裁切源图片、删减部分图片），需将新图片存入指定文件夹内
    '''
    projectId = globalv.get_value('projectId')
    containerId = globalv.get_value('containerId')

    str_time = str(time.strftime('%Y-%m-%d', time.localtime()))
    channel_id = str(img_path).split('/')[-3]

    new_img_dir = os.path.join('./results', projectId, containerId, str_time, channel_id, 'new_img')
    new_img_dir_upload = os.path.join('./results', projectId, containerId, 'new_img_upload')    # 拷贝一份新图片用于传给后端
    os.makedirs(new_img_dir, exist_ok=True)
    os.makedirs(new_img_dir_upload, exist_ok=True)
    crop_info_dict = {'source_img_path': None, 'new_img_path': None, 'crop_point': None}
    new_img_name = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time())).hex)

    temp_dict = crop_info_dict.copy()

    if rect:
        new_img_path = os.path.join(new_img_dir, new_img_name + '.jpg')
        img = cv2.imread(img_path)
        if isinstance(rect, list):
            crop_point = rect
        else:
            crop_point = [rect.左上点.x, rect.左上点.y, rect.右下点.x, rect.右下点.y]

        img_crop = img[crop_point[1]:crop_point[3], crop_point[0]:crop_point[2]]
        cv2.imwrite(new_img_path, img_crop)
        shutil.copyfile(new_img_path, os.path.join(new_img_dir_upload, new_img_name + '.jpg'))

        temp_dict['source_img_path'] = img_path
        temp_dict['new_img_path'] = new_img_path
        temp_dict['crop_point'] = crop_point
    else:
        new_img_path = os.path.join(new_img_dir, new_img_name + str(os.path.splitext(img_path)[-1]))
        shutil.copyfile(img_path, new_img_path)
        shutil.copyfile(img_path, os.path.join(new_img_dir_upload, new_img_name + str(os.path.splitext(img_path)[-1])))
        temp_dict['source_img_path'] = img_path
        temp_dict['new_img_path'] = new_img_path

    # 保存图片间对应关系
    with open(os.path.join('./results', projectId, containerId, 'crop_info.txt'), 'a+') as f:
        f.write(json.dumps(temp_dict) + '\n')


def 映射回原图像(本帧, 全局状态):
    projectId = globalv.get_value('projectId')
    containerId = globalv.get_value('containerId')

    img_path = 本帧.原图
    with open(全局状态.crop_info, 'r') as f:
        crop_info = [json.loads(i) for i in f.readlines()]

    crop_names = [os.path.split(i['new_img_path'])[1] for i in crop_info]
    img_name = os.path.split(img_path)[1]
    idx = crop_names.index(img_name)

    img_source_path = crop_info[idx]['source_img_path']
    top_left_point = crop_info[idx]['crop_point'][:2]
    img = cv2.imread(img_source_path)

    kpt = []
    for i in 本帧.kpt:
        kpt.append([i[0] + top_left_point[0], i[1] + top_left_point[1]])

    show_human_pose(img, kpt, get_color([None] * 17))

    cv2.imwrite(new_img_path, img)





def 绝对值(value):
    return abs(value)



class 点(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def 可视化(self, img=None):
        if isinstance(img, str) and os.path.exists(img):
            img = cv2.imread(img)
        if img is None:
            img = np.full((1080, 1920, 3), 255, np.uint8)
        colors = get_color([None] * 1)
        cv2.circle(img, (int(self.x), int(self.y)), 6, colors[0], -1)
        # 显示
        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        plt.imshow(img[:, :, ::-1])
        plt.show()


class 线段(object):
    def __init__(self, 点1, 点2):
        self.点1 = 点1
        self.点2 = 点2

    # def __call__(self, *args, **kwargs):
    #     return self.长度()

    def 数值(self):
        return round(math.dist([self.点1.x, self.点1.y], [self.点2.x, self.点2.y]), 1)

    def 可视化(self, img=None):
        if isinstance(img, str) and os.path.exists(img):
            img = cv2.imread(img)
        if img is None:
            img = np.full((1080, 1920, 3), 255, np.uint8)
        colors = get_color([None] * 2)
        cv2.circle(img, (int(self.点1.x), int(self.点1.y)), 6, colors[0], -1)
        cv2.circle(img, (int(self.点2.x), int(self.点2.y)), 6, colors[0], -1)
        cv2.line(img, (int(self.点1.x), int(self.点1.y)), (int(self.点2.x), int(self.点2.y)), colors[1], 2)
        # 显示
        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        plt.imshow(img[:, :, ::-1])
        plt.show()


class 三点的夹角(object):
    def __init__(self, 点1, 点2, 点3):
        self.点1 = 点1
        self.点2 = 点2
        self.点3 = 点3

    def 数值(self):
        a = math.sqrt(
            (self.点2.x - self.点3.x) * (self.点2.x - self.点3.x) + (self.点2.y - self.点3.y) * (self.点2.y - self.点3.y))
        b = math.sqrt(
            (self.点1.x - self.点3.x) * (self.点1.x - self.点3.x) + (self.点1.y - self.点3.y) * (self.点1.y - self.点3.y))
        c = math.sqrt(
            (self.点1.x - self.点2.x) * (self.点1.x - self.点2.x) + (self.点1.y - self.点2.y) * (self.点1.y - self.点2.y))
        # A = math.degrees(math.acos((a * a - b * b - c * c) / (-2 * b * c)))
        temp = (b * b - a * a - c * c) / (-2 * a * c)
        temp = min(1, max(-1, temp))  # 保证数值在[-1,1]之间，否则后续计算会越界
        B = math.degrees(math.acos(temp))
        # C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
        return round(B, 1)

    def 可视化(self, img=None):
        if isinstance(img, str) and os.path.exists(img):
            img = cv2.imread(img)
        if img is None:
            img = np.full((1080, 1920, 3), 255, np.uint8)
        colors = get_color([None] * 2)
        cv2.circle(img, (int(self.点1.x), int(self.点1.y)), 6, colors[0], -1)
        cv2.circle(img, (int(self.点2.x), int(self.点2.y)), 6, colors[0], -1)
        cv2.circle(img, (int(self.点3.x), int(self.点3.y)), 6, colors[0], -1)
        cv2.line(img, (int(self.点1.x), int(self.点1.y)), (int(self.点2.x), int(self.点2.y)), colors[1], 2)
        cv2.line(img, (int(self.点2.x), int(self.点2.y)), (int(self.点3.x), int(self.点3.y)), colors[1], 2)
        # 显示
        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        plt.imshow(img[:, :, ::-1])
        plt.show()

    # def __call__(self, *args, **kwargs):
    #     return self.角度()


class 点到直线的距离(object):
    def __init__(self, 点1, 线1):
        self.point = 点1
        self.line = 线1
        self.line_point1 = 线1.点1
        self.line_point2 = 线1.点2
        self.p_foot = 点(0, 0)

    # def 数值(self):
    #     if self.line_point1 == self.line_point2:
    #         point_array = np.array(self.point)
    #         point1_array = np.array(self.line_point1)
    #         return np.linalg.norm(point_array - point1_array)
    #     # 计算直线的三个参数
    #     A = self.line_point2.y - self.line_point1.y
    #     B = self.line_point1.x - self.line_point2.x
    #     C = (self.line_point1.y - self.line_point2.y) * self.line_point1.x + \
    #         (self.line_point2.x - self.line_point1.x) * self.line_point1.y
    #     # 根据点到直线的距离公式计算距离
    #     distance = np.abs(A * self.point.x + B * self.point.y + C) / (np.sqrt(A ** 2 + B ** 2))
    #     return round(distance, 2)

    def 获取垂足(self):
        start_x, start_y = self.line_point1.x, self.line_point1.y
        end_x, end_y = self.line_point2.x, self.line_point2.y
        pa_x, pa_y = self.point.x, self.point.y

        if start_x == end_x:
            self.p_foot.x = start_x
            self.p_foot.y = pa_y
            return self.p_foot

        k = (end_y - start_y) * 1.0 / (end_x - start_x)
        a = k
        b = -1.0
        c = start_y - k * start_x
        self.p_foot.x = int((b * b * pa_x - a * b * pa_y - a * c) / (a * a + b * b))
        self.p_foot.y = int((a * a * pa_y - a * b * pa_x - b * c) / (a * a + b * b))

        return self.p_foot

    def 数值(self):
        self.p_foot = self.获取垂足()
        distance = 线段(self.point, self.p_foot).数值()
        return round(distance, 2)

    def 可视化(self, img=None):
        if isinstance(img, str) and os.path.exists(img):
            img = cv2.imread(img)
        if img is None:
            img = np.full((1080, 1920, 3), 255, np.uint8)
        colors = get_color([None] * 4)
        cv2.circle(img, (int(self.point.x), int(self.point.y)), 6, colors[0], -1)
        cv2.circle(img, (int(self.line_point1.x), int(self.line_point1.y)), 6, colors[0], -1)
        cv2.circle(img, (int(self.line_point2.x), int(self.line_point2.y)), 6, colors[0], -1)
        cv2.circle(img, (int(self.p_foot.x), int(self.p_foot.y)), 10, colors[1], -1)
        cv2.line(img, (int(self.line_point1.x), int(self.line_point1.y)), (int(self.line_point2.x), int(self.line_point2.y)), colors[2], 2)
        cv2.line(img, (int(self.point.x), int(self.point.y)), (int(self.p_foot.x), int(self.p_foot.y)), colors[3], 2)
        # 显示
        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        plt.imshow(img[:, :, ::-1])
        plt.show()


class 矩形(object):
    def __init__(self, 点1, 点2):
        self.左上点 = 点1
        self.右下点 = 点2
        self.长 = abs(点1.x - 点2.x)
        self.宽 = abs(点1.y - 点2.y)
        self.右上点 = 点(点2.x, 点1.y)
        self.左下点 = 点(点1.x, 点2.y)

    def 周长(self):
        return (self.长 + self.宽) * 2

    def 面积(self):
        return self.长 * self.宽

    def 中心点(self):
        return 点((self.左上点.x + self.右下点.x) / 2, (self.左上点.y + self.右下点.y) / 2)

    def 可视化(self, img=None):
        if isinstance(img, str) and os.path.exists(img):
            img = cv2.imread(img)
        if img is None:
            img = np.full((1080, 1920, 3), 255, np.uint8)

        cv2.rectangle(img, (self.左上点.x, self.左上点.y), (self.右下点.x, self.右下点.y), (128, 128, 0), 3, cv2.LINE_AA)
        # 显示
        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        plt.imshow(img[:, :, ::-1])
        plt.show()


def 两矩形重合度(矩形1, 矩形2):
# def compute_IOU(rec1, rec2):
    """
    计算两个矩形框的交并比。
    :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
    :param rec2: (x0,y0,x1,y1)
    :return: 交并比IOU.
    """
    if isinstance(矩形1, list) or isinstance(矩形1, tuple):
        rec1 = 矩形1
    if isinstance(矩形2, list) or isinstance(矩形2, tuple):
        rec2 = 矩形2
    if isinstance(矩形1, 矩形):
        rec1 = (矩形1.左上点.x, 矩形1.左上点.y, 矩形1.右下点.x, 矩形1.右下点.y)
    if isinstance(矩形2, 矩形):
        rec2 = (矩形2.左上点.x, 矩形2.左上点.y, 矩形2.右下点.x, 矩形2.右下点.y)

    left_column_max = max(rec1[0], rec2[0])
    right_column_min = min(rec1[2], rec2[2])
    up_row_max = max(rec1[1], rec2[1])
    down_row_min = min(rec1[3], rec2[3])
    # 两矩形无相交区域的情况
    if left_column_max >= right_column_min or down_row_min <= up_row_max:
        return 0
    # 两矩形有相交区域的情况
    else:
        S1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        S2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
        S_cross = (down_row_min - up_row_max) * (right_column_min - left_column_max)
        return round(S_cross / (S1 + S2 - S_cross), 2)


class 目标检测结果:
    def __init__(self, category, rect, confidence):
        self.rect = rect
        self.类别名称 = category
        self.矩形框 = 矩形(点(rect[0], rect[1]), 点(rect[2], rect[3]))
        self.置信度 = confidence

    def 可视化(self, img=None, threshold=0.1):
        if img is None:
            img = np.full((1080, 1920, 3), 255, np.uint8)
        else:
            img = cv2.imread(img)
        img = show_object_detection(img, [[0, *self.rect, self.置信度]], [self.类别名称], [[128, 128, 0]], threshold=threshold)

        # 显示
        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        plt.imshow(img[:, :, ::-1])
        plt.show()


class 人:
    def __init__(self, kpt):
        self.kpt = kpt
        self.鼻子 = 点(kpt[0][0], kpt[0][1])
        self.左眼 = 点(kpt[1][0], kpt[1][1])
        self.右眼 = 点(kpt[2][0], kpt[2][1])
        self.左耳 = 点(kpt[3][0], kpt[3][1])
        self.右耳 = 点(kpt[4][0], kpt[4][1])
        self.左肩 = 点(kpt[5][0], kpt[5][1])
        self.右肩 = 点(kpt[6][0], kpt[6][1])
        self.左手肘 = 点(kpt[7][0], kpt[7][1])
        self.右手肘 = 点(kpt[8][0], kpt[8][1])
        self.左手腕 = 点(kpt[9][0], kpt[9][1])
        self.右手腕 = 点(kpt[10][0], kpt[10][1])
        self.左臀 = 点(kpt[11][0], kpt[11][1])
        self.右臀 = 点(kpt[12][0], kpt[12][1])
        self.左膝盖 = 点(kpt[13][0], kpt[13][1])
        self.右膝盖 = 点(kpt[14][0], kpt[14][1])
        self.左脚踝 = 点(kpt[15][0], kpt[15][1])
        self.右脚踝 = 点(kpt[16][0], kpt[16][1])

    def 可视化(self, img=None, threshold=0.1):
        if img is None:
            img = np.full((1080, 1920, 3), 255, np.uint8)
        else:
            img = cv2.imread(img)
        colors = get_color([None] * 17)
        show_human_pose(img, self.kpt, colors, threshold)

        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        plt.imshow(img[:, :, ::-1])
        plt.show()


class 单帧(object):
    def __init__(self, frame_result, label_names):
        self.label_names = label_names
        self.img_path = frame_result['img_path']
        self.原图 = self.img_path
        self.json_path = frame_result['json_path']
        self.warn_path = frame_result['warn_path']
        self.channelId = frame_result['channelId']
        self.cameraUrl = frame_result['cameraUrl']

        if self.json_path:
            with open(self.json_path, 'r') as f:
                self.json_ret = json.loads(f.read())

            # 若为人体关键点
            if self.json_ret and len(self.json_ret[0]) == 17 and len(self.json_ret[0][0]) == 3:
                self.label_category = 1
                self.kpt = self.json_ret[0]
                self.人 = 人(self.kpt)   # 目前默认检测单人

            # 若为目标检测
            elif self.json_ret and len(self.json_ret[0]) == 6 and type(self.json_ret[0][0]) is int:
                self.label_category = 2
                self.结果 = [目标检测结果(label_names[i[0]], [i[1], i[2], i[3], i[4]], i[5]) for i in self.json_ret]


    def 可视化(self, img=None, category=None, threshold=0.1):
        # print(self.img_path)
        if img is None:
            img = cv2.imread(self.img_path)
        else:
            img = cv2.imread(img)
        colors = get_color(self.label_names)

        # 1为人体关键点, 2为目标检测
        if self.label_category == 1:
            show_human_pose(img, self.kpt, colors, threshold)

        elif self.label_category == 2:
            img = show_object_detection(img, self.json_ret, self.label_names, colors, category=category, threshold=threshold)

        # 显示
        # cv2.imshow('frame', img)
        # cv2.waitKey(0)
        plt.imshow(img[:, :, ::-1])
        plt.show()



class Init():
    def __init__(self, node_result_path, label_names_path):
        with open(node_result_path, 'r') as f:
            self.node_result = json.loads(f.read())
        with open(label_names_path, 'r') as f:
            self.标签名称 = json.loads(f.read())

        self.num_ret = len(self.node_result)
        self.idx = 0

        self.上一帧 = None

        img_dir = os.path.split(node_result_path)[0]
        self.crop_info = None
        crop_info_path = os.path.join(img_dir, 'crop_info.txt')
        try:
            str_time = [i for i in os.listdir(img_dir) if re.search(r'\d+-\d+-\d+', i)][-1]
            channel = os.listdir(os.path.join(img_dir, str_time))[0]
            if os.path.exists(os.path.join(img_dir, str_time, channel, 'json')):
                self.is_logic_node = False
            else:
                self.is_logic_node = True
                if os.path.exists(crop_info_path):
                    self.crop_info = crop_info_path
        except:
            self.is_logic_node = True
            if os.path.exists(crop_info_path):
                self.crop_info = crop_info_path


    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < self.num_ret:
            frame_result = self.node_result[self.idx]
            frame = 单帧(frame_result, self.标签名称)
            self.上一帧 = frame
            self.idx += 1
            return frame

        else:
            raise StopIteration

    def 可视化(self, value):
        print(value)


if __name__ == '__main__':
    # with open('results/123/node_result.txt', 'r') as f:
    #     node_result = json.loads(f.read())
    # with open('results/123/label_names.txt', 'r') as f:
    #     label_names = json.loads(f.read())


    with open('results/86d08e2ca6335d87b4aff6778033e453/9a7fa8a8920c4795bbdc82c4e4dd7a6d/node_result.txt', 'r') as f:
        node_result = json.loads(f.read())
    with open('results/86d08e2ca6335d87b4aff6778033e453/9a7fa8a8920c4795bbdc82c4e4dd7a6d/label_names.txt', 'r') as f:
        label_names = json.loads(f.read())


    推理结果 = Init(node_result, label_names)
    for 本帧 in 推理结果:

        # 本帧.可视化()

        for 结果 in 本帧.结果:
            结果.可视化(本帧.原图)
