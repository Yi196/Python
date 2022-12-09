import json
import os
import shutil
import copy
import cv2
import uuid


def dHash(img):
    # 差值哈希算法
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j+1]:
                hash_str = hash_str+'1'
            else:
                hash_str = hash_str+'0'
    return hash_str


def json2codeX(json_path, label_names):
    with open(json_path, 'r') as f:
        json_value = json.loads(f.read())

    ret = {'label_box2D': []}
    label_dict = {"number": None, "instanceId": None, "box2D": {"ymin": None, "xmin": None, "ymax": None, "xmax": None}, "attributes": {}, "category": None}

    num = 0
    for i in json_value:
        num += 1
        d = copy.deepcopy(label_dict)
        d["number"] = num
        d["instanceId"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(i)))
        d["box2D"]["xmin"] = str(i[1])
        d["box2D"]["ymin"] = str(i[2])
        d["box2D"]["xmax"] = str(i[3])
        d["box2D"]["ymax"] = str(i[4])
        d["category"] = label_names[int(i[0])]

        ret['label_box2D'].append(d)

    return ret


def find_diff_img(img_input, num_picture=50, thresh=10):
    if type(img_input) is str:
        is_dir = True
        img_dir = img_input
        img_names = os.listdir(img_dir)
    else:
        is_dir = False
        img_names = img_input

    img_dhash_lst = []
    for idx, i in enumerate(img_names):
        if is_dir:
            img = cv2.imread(os.path.join(img_dir, i))
        else:
            img = cv2.imread(i)
        temp = dHash(img)
        img_dhash_lst.append('0b' + temp)

    value_lst = []
    for idx, i in enumerate(img_dhash_lst):
        if not i:
            continue
        for jdx, j in enumerate(img_dhash_lst[idx + 1:]):
            if not j:
                continue
            dif_num = str(bin(eval(i) ^ eval(j))).count('1')  # 0-64 越小图像差别越小
            # print(dif_num)
            if dif_num < thresh:
                img_dhash_lst[idx + jdx + 1] = None
            else:
                value_lst.append([dif_num, idx, idx + jdx + 1])  # [相似度，1图片索引，2图片索引]
    # print(value_lst)

    # 跟据相似度排序
    value_lst.sort(key=lambda x: x[0], reverse=True)
    # print(value_lst)

    ret_lst = []
    for (_, idx1, idx2) in value_lst:
        if idx1 not in ret_lst:
            ret_lst.append(idx1)
        if idx2 not in ret_lst:
            ret_lst.append(idx2)
        if len(ret_lst) >= num_picture:
            ret_lst = ret_lst[:num_picture]
            break

    img_path_lst = []
    for img_idx in ret_lst:
        if is_dir:
            img_path_lst.append(os.path.join(img_dir, img_names[img_idx]))
        else:
            img_path_lst.append(img_names[img_idx])

    return img_path_lst



def save_diff_img(img_data_dir, num_picture=50, thresh=10):

    '''
    查找差异最大的图片，存入指定文件夹
    :param img_data_dir: 图片地址，给到日期（会自动遍历该日期下所有通道）
    :param num_picture: 获取图片最大数量
    :param thresh: 小于阈值，相似度较高的图片直接过滤
    :return: None
    '''

    # 获取通道id
    channel_id_lst = [i for i in os.listdir(img_data_dir) if os.path.isdir(os.path.join(img_data_dir, i))]

    # 判断是否为推理节点
    if not os.path.exists(os.path.join(img_data_dir, channel_id_lst[0], 'source')):
        print('It is not a inference node, program will do nothing')
        return

    save_dir = str(img_data_dir).replace('/results/', '/dataCollect/')
    os.makedirs(save_dir, exist_ok=True)

    # 读取标签名称
    with open(os.path.join(os.path.abspath(os.path.join(img_data_dir, '..')), 'label_names.txt'), 'r') as f:
        label_names = json.loads(f.read())

    # 先从每个通道提取差异最大的num_picture张图片，合并后再次提取，以减小计算量
    channel_img_lst = []
    for channel_id in channel_id_lst:
        img_dir = os.path.join(img_data_dir, channel_id, 'source')
        channel_img_lst.extend(find_diff_img(img_dir, num_picture, thresh))

    img_path_lst = find_diff_img(channel_img_lst, num_picture, thresh)

    for img_path in img_path_lst:
        shutil.copyfile(img_path, os.path.join(save_dir, os.path.split(img_path)[1]))

        temp = str(img_path).replace('/source/', '/json_copy/')
        idx = temp.rfind('.')
        json_path = temp[:idx] + '.json'
        # print(json_path)

        if os.path.exists(json_path):
            # 转为开发平台标注格式，并存入指定文件夹
            json_codex = json2codeX(json_path, label_names)
            with open(os.path.join(save_dir, os.path.split(json_path)[1]), 'w') as f:
                f.write(json.dumps(json_codex))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='find different images')
    parser.add_argument('--img_data_dir', type=str)
    args = parser.parse_args()

    save_diff_img(args.img_data_dir)

    # img_data_dir = '/home/mafneg/桌面/img_test/12-15'
    # save_dir = '/home/mafneg/桌面/img_test/save'
    # save_diff_img(img_data_dir, save_dir)
