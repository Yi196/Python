import json
import os.path
import time
import cv2
import base64
import requests
import numpy as np


# 益趣相关参数
eacheart_config = {'base_url': 'http://platform.eacheart.com:9099',
                   'garbage_retention_url': '/api/1.0/project/aiDistinguish/garbageBagRetention',
                   'garbage_clean_url': '/api/1.0/project/aiDistinguish/garbageBagClean',
                   'get_monitors_url': '/api/1.0/project/aiDistinguish/cameraList',
                   'key': 'e24d07c20783743e16ded6630c7ece0c',
                   'secret': '8df989f4b3e9b0319db41b3b2f3789b2'
                   }

def get_monitors():
    data = json.dumps({'key': eacheart_config['key'], 'secret': eacheart_config['secret'], 'timeStamp': str(int(time.time() * 1000))})

    monitors_info = requests.post(eacheart_config['base_url'] + eacheart_config['get_monitors_url'], data=data, headers={'Content-Type': 'application/json'}).json()
    # print(monitors_info)
    return {k['cameraUrl']: k['cameraId'] for k in monitors_info['data']}


def create_result(ret, cameraId):
    img_source = cv2.imread(ret['img_path'])
    img_draw = img_source.copy()
    with open(ret['json_path'], 'r') as f:
        labels = json.loads(f.read())

    for l in labels:
        c1, c2 = (int(l[1]), int(l[2])), (int(l[3]), int(l[4]))
        cv2.rectangle(img_draw, c1, c2, (0, 0, 255), thickness=3, lineType=cv2.LINE_AA)

    _, buffer = cv2.imencode('.jpg', img_draw)
    image_byte = base64.b64encode(buffer)
    aiPic = str(image_byte, encoding='utf-8')

    _, buffer_ori = cv2.imencode('.jpg', img_source)
    image_byte_ori = base64.b64encode(buffer_ori)
    oriPic = str(image_byte_ori, encoding='utf-8')

    garbage_retention = {
        'cameraId': cameraId,
        'aiPic': aiPic,
        'timeStamp': str(int(time.time() * 1000)),
        'remark1': oriPic,
        'remark2': '...',
        'remark3': '...'
    }
    return garbage_retention


def logic(cfg):
    local_names = locals()
    for idx, i in enumerate(cfg['previous_node_result_path']):
        with open(i, 'r') as f:  # 之前节点的结果
            local_names[f'previous_node_result_{idx}'] = json.loads(f.read())
    for idx, i in enumerate(cfg['previous_label_names_path']):
        with open(i, 'r') as f:  # 感知节点的标签名称
            local_names[f'previous_label_names_{idx}'] = json.loads(f.read())
    if os.path.exists(cfg['global_status_path']):
        with open(cfg['global_status_path'], 'r') as f:  # 最后一个节点的结果，也是之前流程的结果
            global_status = f.readlines()

    previous_node_result = local_names['previous_node_result_0']
    label_names = local_names['previous_label_names_0']
    global_status_path = cfg['global_status_path']

    person_idx = -1
    no_trash_idx = -1
    if 'xingren' in label_names:
        person_idx = label_names.index('xingren')
        no_trash_idx = label_names.index('feilajibao')
    elif '行人' in label_names:
        person_idx = label_names.index('行人')
        no_trash_idx = label_names.index('非垃圾包')

    # 去除含人的结果、 去除非垃圾包的标签结果
    for idx, i in enumerate(previous_node_result):
        if i['json_path']:
            json_path = i['json_path']
            with open(json_path, 'r') as f:
                labels = json.loads(f.read())
            label = [int(l[0]) for l in labels]
            if person_idx in label:          # 含有人时直接跳过
                previous_node_result[idx]['json_path'] = None
                continue
            if no_trash_idx in label:        # 去除非垃圾包的标签结果
                len_label = len(label)
                for x, y in enumerate(label[::-1]):
                    if y == no_trash_idx:
                        x = len_label - x - 1
                        labels.pop(x)
                if labels:
                    with open(json_path, 'w') as f:
                        f.write(json.dumps(labels))
                else:
                    previous_node_result[idx]['json_path'] = None
    # print(previous_node_result)


    # 每五轮向益趣发送一次结果，注意第五次结果会被写在第一行 故每5行取后4行
    if len(global_status) < 5:
        return previous_node_result

    before_result_lst = [json.loads(i) for i in global_status[-4:]]
    before_result_lst.append(previous_node_result)

    # 获取益趣的cameraId
    cfg['eacheart_cameraId'] = get_monitors()

    last_warn_path = os.path.join(os.path.split(global_status_path)[0], 'last_warn.txt')   # 上次向益趣发送的结果信息
    if os.path.exists(last_warn_path):
        with open(last_warn_path, 'r') as f:
            last_warn_result = json.loads(f.read())
        if len(last_warn_result) != len(previous_node_result):
            last_warn_result = []
    else:
        last_warn_result = []

    num_detect = [0] * len(previous_node_result)

    for r in before_result_lst:
        for idx, i in enumerate(r):
            if i['json_path']:
                num_detect[idx] += 1
    # print(num_detect)

    trash_retention_list = []
    trash_clean_list = []
    for idx, num in enumerate(num_detect):
        cameraId = cfg['eacheart_cameraId'][f'{previous_node_result[idx]["cameraUrl"]}'] \
            if previous_node_result[idx]['cameraUrl'] in cfg['eacheart_cameraId'] else None
        if last_warn_result:
            if num > 3:
                result = previous_node_result[idx] if previous_node_result[idx]['json_path'] else before_result_lst[3][idx]
                result = result if result['json_path'] else before_result_lst[2][idx]
                if last_warn_result[idx]:   # 已经告警过
                    previous_node_result[idx]['json_path'] = None
                else:
                    previous_node_result[idx] = result
                    last_warn_result[idx] = True
                    # '''trash appear'''
                    trash_retention_list.append(create_result(result, cameraId))

            else:
                # 排除未取到图情况
                if sum([bool(i[idx]['img_path']) for i in before_result_lst]) < 4:
                    previous_node_result[idx]['json_path'] = None
                    continue
                previous_node_result[idx] = previous_node_result[idx] if previous_node_result[idx]['img_path'] else before_result_lst[3][idx]
                previous_node_result[idx]['json_path'] = None
                if last_warn_result[idx]:
                    last_warn_result[idx] = False
                    # '''trash disappear'''
                    trash_clean_list.append({'cameraId': cameraId, 'timeStamp': str(int(time.time()*1000))})
                    # 垃圾消失时也向后端告警
                    json_p = previous_node_result[idx]['img_path'][:-3] + 'json'
                    json_p = str(json_p).replace('source', 'json')
                    previous_node_result[idx]['json_path'] = json_p
                    with open(json_p, 'w') as f:
                        f.write(json.dumps([]))

        else:   # run first time
            if num > 3:
                result = previous_node_result[idx] if previous_node_result[idx]['json_path'] else before_result_lst[3][idx]
                result = result if result['json_path'] else before_result_lst[2][idx]
                previous_node_result[idx] = result
                # '''trash appear'''
                trash_retention_list.append(create_result(result, cameraId))

            else:
                previous_node_result[idx]['json_path'] = None

    # print(trash_retention_list)
    # print(trash_clean_list)
    # 向益趣发送检测结果
    if len(trash_retention_list) > 0:
        msg = requests.post(eacheart_config['base_url'] + eacheart_config['garbage_retention_url'], data=json.dumps(trash_retention_list), headers={'Content-Type': 'application/json'})
        print(msg, msg.json())

    if len(trash_clean_list) > 0:
        msg = requests.post(eacheart_config['base_url'] + eacheart_config['garbage_clean_url'], data=json.dumps(trash_clean_list), headers={'Content-Type': 'application/json'})
        print(msg, msg.json())

    # 每五轮发送一次结果, 并清空之前记录
    with open(global_status_path, 'w') as f:
        f.write('')

    # 保存本次结果的状态
    if not last_warn_result:
        last_warn_result = [bool(i['json_path']) for i in previous_node_result]
    with open(last_warn_path, 'w') as f:
        f.write(json.dumps(last_warn_result))

    # print(previous_node_result)
    return previous_node_result

if __name__ == '__main__':
    cfg = {'global_status_path': r'results/ff808181837e1b4201837e2cb8200000/global_status.txt',
           'previous_node_result': [{'img_path': './results/ff808181837e1b4201837e2cb8200000/ff808181826819480182682053ff0004/2022-09-27/source/2022-09-27-21-52-48.jpg', 'json_path': './results/ff808181837e1b4201837e2cb8200000/ff808181826819480182682053ff0004/2022-09-27/json/2022-09-27-21-52-48.json', 'warn_path': './results/ff808181837e1b4201837e2cb8200000/ff808181826819480182682053ff0004/2022-09-27/warn/2022-09-27-21-52-48.jpg', 'channelId': 'ff808181826819480182682053ff0004', 'cameraUrl': 'https://video.eacheart.com:447/eacheart-video-space/31011500991320014097.m3u8?e=1665911434&token=86098306fd480abf299e88c359a6ac91'}],
           'label_names': ['行人', '垃圾包', '非垃圾包']}

    logic(cfg)