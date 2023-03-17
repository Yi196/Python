# https://blog.csdn.net/weixin_46504244/article/details/121982890
# https://zhuanlan.zhihu.com/p/74260950

''' 确保自己已经安装了ffmpeg ,而且ffmpeg已经和nginx配置好 '''


# 摄像头实时推流、实时图片序列推流
import cv2
import queue
import os
import numpy as np
from threading import Thread
import datetime, _thread
import subprocess as sp
from time import *

# 使用线程锁，防止线程死锁
mutex = _thread.allocate_lock()
# 存图片的队列
frame_queue = queue.Queue()
# 推流的地址，前端通过这个地址拉流，主机的IP，1935是ffmpeg在nginx中设置的端口号
rtmpUrl = "rtmp://139.159.142.192:1935/live/1"

# 用于推流的配置,参数比较多，可网上查询理解
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(640, 480),  # 图片分辨率
           '-r', str(25.0),  # 视频帧率
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmpUrl]


def Video():
    # 调用相机拍图的函数
    vid = cv2.VideoCapture(r"/usr/local/web/studey/mysite/chat/video/4.mp4")
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
    while (vid.isOpened()):
        return_value, frame = vid.read()
        # 原始图片推入队列中
        frame_queue.put(frame)


def push_frame():
    # 推流函数
    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = time()

    # 防止多线程时 command 未被设置
    while True:
        if len(command) > 0:
            # 管道配置，其中用到管道
            p = sp.Popen(command, stdin=sp.PIPE)
            break

    while True:
        if frame_queue.empty() != True:
            # 从队列中取出图片
            frame = frame_queue.get()
            # curr_time = timer()
            # exec_time = curr_time - prev_time
            # prev_time = curr_time
            # accum_time = accum_time + exec_time
            # curr_fps = curr_fps + 1

            # process frame
            # 你处理图片的代码
            # 将图片从队列中取出来做处理，然后再通过管道推送到服务器上
            # 增加画面帧率
            # if accum_time > 1:
            # accum_time = accum_time - 1
            # fps = "FPS: " + str(curr_fps)
            # curr_fps = 0

            # write to pipe
            # 将处理后的图片通过管道推送到服务器上,image是处理后的图片
            p.stdin.write(frame.tostring())


def run():
    # 使用两个线程处理
    thread1 = Thread(target=Video, )
    thread1.start()
    thread2 = Thread(target=push_frame, )
    thread2.start()


# if __name__ == '__main__':
#     run()


# 视频推流
import cv2
import subprocess

src = "/usr/local/web/studey/mysite/chat/video/4.mp4"
rtmp = 'rtmp://127.0.0.1:1935/live/1'
cap = cv2.VideoCapture(src)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
size = (int(640), int(480))
sizeStr = str(size[0]) + 'x' + str(size[1])

command = ['ffmpeg',
           '-y', '-an',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', sizeStr,
           '-r', '25',
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmp]

pipe = subprocess.Popen(command
                        , shell=False
                        , stdin=subprocess.PIPE
                        )

while cap.isOpened():
    success, frame = cap.read()
    if success == False:
        print("Err")
        break
    img = cv2.resize(frame, size)
    pipe.stdin.write(img.tostring())
cap.release()
pipe.terminate()




###################################################
# 按照固定帧推流
'''
只能用于长度固定的视频文件
因为对于视频流cap.get(cv2.CAP_PROP_POS_MSEC) 一直为0
'''
import time
import cv2
import subprocess as sp

class Live(object):
    def __init__(self, camera_path, rtmpUrl, cfg):
        self.cap = cv2.VideoCapture(camera_path)

        if not self.cap.isOpened():
            raise ConnectionError(f'Can not open {camera_path}')

        self.camera_start_time = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.process_start_time = time.time() * 1000  # ms
        self.next_time = self.process_start_time

        fps = 10
        self.interval = 1000. / fps  # ms

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # ffmpeg command
        self.command = ['ffmpeg',
                '-y',
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-pix_fmt', 'bgr24',
                '-s', "{}x{}".format(width, height),
                '-r', str(fps),
                '-i', '-',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'ultrafast',
                '-f', 'flv',
                rtmpUrl]

    def push_frame(self):
        # 管道配置  防止多线程时command未被设置
        while True:
            p = sp.Popen(self.command, stdin=sp.PIPE)
            break

        _, frame = self.cap.read()
        while True:
            # 检测图片并绘制检测结果
            frame = self.model.detect_draw(frame)

            # write to pipe
            p.stdin.write(frame.tostring())

            # 根据帧数取图
            self.next_time = max(time.time() * 1000, self.next_time + self.interval)
            while self.cap.get(cv2.CAP_PROP_POS_MSEC) - self.camera_start_time + self.process_start_time < self.next_time:
                self.cap.grab()
            _, frame = self.cap.retrieve()


##############################################################
'''
视频流 转推 每次只获取最新帧
'''

import os
import threading
import time
import cv2
import subprocess as sp
import json
import importlib
import traceback
import queue


class Live(object):
    def __init__(self, camera_path, rtmpUrl, cfg):
        self.model = None
        self.video = False
        self.camera_path = camera_path
        self.cfg = cfg
        self.init_image = cv2.imread(r'tools/init_image.jpg')

        self.next_time = time.time() * 1000  # ms
        self.fps = 5
        self.interval = 1000. / self.fps  # ms
        # width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(960)
        self.height = int(600)

        # ffmpeg command
        # self.command = ['ffmpeg',       # arm版使用容器中安装的ffmpeg
        self.command = ['tools/ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(self.width, self.height),
                        '-r', str(self.fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        rtmpUrl]

        # 始终读取最新帧
        self.q = queue.Queue(self.fps * 10)
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()
        # 多线程加载模型
        t = threading.Thread(target=self._init_model)
        t.daemon = True
        t.start()


    def _init_model(self):
        self.cap = cv2.VideoCapture(self.camera_path)
        if self.cap.isOpened():
            self.fps_input = self.cap.get(5)
            if not (0<= self.fps_input <= 30):
                self.fps_input = 25

            try:
                if self.cfg['nodeCategory'] == 1:  # 1:目标检测  2:语义分割  3:姿态估计  4: 图像分类
                    self.model = importlib.import_module('inference_node_yolov7').Init_mode_Yolov7(self.cfg)
                elif self.cfg['nodeCategory'] == 4:
                    self.model = importlib.import_module('inference_mmclassification').Init_mode_MMclassification(self.cfg)
                self.video = True

            except:
                self.init_image = cv2.putText(self.init_image, "Error: Can not load model!!!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 20)
                raise ValueError('Can not load model!')

        else:
            self.init_image = cv2.imread(r'tools/video_error.jpg')

    def _reader(self):
        temp = 0
        count = 0
        first = True
        while True:
            if self.video:
                if first:
                    skip_num = self.fps_input / self.fps
                    skip_num = skip_num - 0.1 if skip_num - 0.1 > 0 else 0
                    print('!!!!!!!!!skip_num:', skip_num)
                    first = False
                    self.q.queue.clear()

                _, frame = self.cap.read()
                count += 1

                if count < temp:
                    if not self.q.empty():  # 缓存足够多时才调帧
                        continue
                else:
                    temp += skip_num

            else:
                # 模型初始化完成前, 推出预览图
                frame = self.init_image
                time.sleep(self.interval / 1000)

            if self.q.full():
                self.q.get()

            self.q.put(frame)

    def push_frame(self):
        # 管道配置  防止多线程时command未被设置
        while True:
            pipe = sp.Popen(self.command, stdin=sp.PIPE)
            break

        while True:
            start_time = time.time()

            # 检测图片并绘制检测结果
            frame = self.q.get()
            if self.model:
                frame = self.model.detect_draw(frame)

            frame = cv2.resize(frame, (self.width, self.height))

            # poll()返回该子进程的状态，0正常结束，1sleep，2子进程不存在，-15 kill，None正在运行
            if pipe.poll() is not None:
                print(pipe.poll())
                print("the popen of ffmpeg not run, try restart")
                pipe = sp.Popen(self.command, stdin=sp.PIPE)
                time.sleep(0.5)

            try:
                # write to pipe
                pipe.stdin.write(frame.tostring())
            except BrokenPipeError:
                print("Pushing the camera appear ERROR")
                print(traceback.format_exc())

            use_time = (time.time() - start_time) * 1000
            # 处理速度较大 FPS较小时, 等待
            self.next_time = max(time.time() * 1000, self.next_time + self.interval)
            while time.time() * 1000 < self.next_time - use_time:
                time.sleep(0.005)

        pipe.stdin.close()  # 关闭输入管道
        pipe.communicate()  # 等待子进程关闭


def detect_real_time(cfg):
    channel_show_id = cfg['previewId']
    rtmpUrl = cfg['rtmpUrl'] + channel_show_id + '00'
    channel_info = [i for i in cfg['algorithmConfigs'] if i['channelId'] == channel_show_id][0]
    rtspAddr = channel_info['rtspAddress']
    cfg['confidence_real_time'] = channel_info['confidence']
    cfg['polygon_real_time'] = [i['points'] for i in (json.loads(channel_info['rectangleRange']) if channel_info['rectangleRange'] else [])]
    Live(rtspAddr, rtmpUrl, cfg).push_frame()