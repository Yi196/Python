import os
import time

import cv2
import sys
import json
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_img(rtsp):
    '''
    param rtsp: [url, channel_id]
    return: img
    '''
    cap = cv2.VideoCapture(rtsp[0])
    count = 0
    while cap.isOpened() and count < 5:
        ret, frame = cap.read()
        if ret:
            break
        else:
            count += 1
    cap.release()

    if ret:
        save_dir = os.path.join(save_img_path, rtsp[1])
        # 超过10张图片，删除最早一张
        if len(os.listdir(save_dir)) > 9:
            min_name = 99999999999999
            for i in os.listdir(save_dir):
                temp = int(os.path.splitext(i)[0])
                if temp < min_name:
                    min_name = temp
            os.remove(os.path.join(save_dir, f'{min_name}.jpg'))

        cv2.imwrite(os.path.join(save_dir, f'{img_name}.jpg'), frame)

    return None


def main(dict_channel):
    rtsp_lst = [[d['url'], d['id']] for d in dict_channel]
    # 创建对应通道文件夹
    for i in rtsp_lst:
        id = i[1]
        os.makedirs(os.path.join(save_img_path, id), exist_ok=True)

    # 使用线程池从所有url获取图片
    with ThreadPoolExecutor() as pool:
        pool.map(get_img, rtsp_lst, timeout=20)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='deployment starts')
    parser.add_argument('--channel_info', type=str)
    args = parser.parse_args()

    save_img_path = r'./photoes/channel_images'
    img_name = str(int(time.time()))

    dict_channel = json.loads(args.channel_info)
    # print(dict_channel)
    main(dict_channel)

