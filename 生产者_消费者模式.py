import threading
from multiprocessing import Process, Queue, Lock
from threading import Thread

from 常用模块.redis_singleton import Queue_Singleton, Redis_subscribe
import random
import time


# lock = Lock()

''' pickle无法序列化自定义数据结构Redis_subscribe中的Redis，会报错：can't pickle _thread.lock objects
    需要将Redis_subscribe设置为全局变量'''

RS = None

# 生产者 每0.5秒生产一个
class Capture(Process):
    def __init__(self, cam_id):
        super(Capture, self).__init__()
        self.cam_id = cam_id
        global RS
        self.queue = Queue_Singleton()
        self.redis_bd = RS
        self.roi_queue = eval(f'self.queue.roi_queue_{cam_id}')
        self.capt = False

    def capture(self):
        for item in self.redis_bd.subscribe().listen():
            if item['type'] == 'message' and item['data'] == '1':
                self.capt = True

    def run(self) -> None:
        count = 1
        get_sub = Thread(target=self.capture, args=())
        get_sub.setDaemon(True)
        get_sub.start()

        while True:
            if self.capt:
                try:
                    roi = random.randint(0,4)
                    # print(roi)
                    self.roi_queue.put({'cam_id': self.cam_id, 'count': count, 'value': roi})
                    count += 1
                    self.capt = False
                    time.sleep(0.5)
                except:
                    pass


# 消费者 每0.8秒处理一个 故每个生产者需配两个消费者
class Detect(Process):
    def __init__(self, cam_id):
        super(Detect, self).__init__()
        self.cam_id = cam_id
        self.queue = Queue_Singleton()
        global RS
        self.redis_db = RS
        self.roi_queue = eval(f'self.queue.roi_queue_{cam_id}')
        self.ret_queue = eval(f'self.queue.ret_queue_{cam_id}')

    def run(self) -> None:
        while True:
            try:
                roi = self.roi_queue.get()
                roi['value'] = bool(roi['value'])
                self.ret_queue.put(roi)
                time.sleep(0.8)
            except:
                pass


class Control_main(Process):
    def __init__(self, cam_num):
        super(Control_main, self).__init__()
        self.cam_num = cam_num
        self.ret_lst = [None] * cam_num  # 结果列表，用来确定所有相机结果都检测完
        self.part_lst = [True] * 6       # 假设剔料位置为0,1 相机检测位置为-1，-2，-3
        self.queue = Queue_Singleton()
        global RS
        self.redis_db = RS
        for i in range(cam_num):
            ret_merge = Thread(target=self._ret_merge, args=(eval(f'self.queue.ret_queue_{i}')))
            ret_merge.setDaemon(True)
            ret_merge.start()

    def _ret_merge(self, queue):
        while True:
            item = queue.get()
            self.ret_lst[item['cam_id']] = item['value']
            if item['cam_id'] == 0:
                self.count = item['count']

    def run(self) -> None:
        while True:
            # 此处可单开一个线程接收PLC消息
            self.part_lst.extend([True, True])
            self.part_lst = self.part_lst[-6:]
            self.redis_db.publish('1')
            while True:
                if None not in self.ret_lst:
                    for idx, i in enumerate(self.ret_lst):
                        self.part_lst[-(idx+1)] = self.part_lst[-(idx+1)] and i

                    print(self.part_lst[0], self.part_lst[1])

                    self.ret_lst = [None] * self.cam_num
                else:
                    time.sleep(0.2)



class Start_all(object):
    def __init__(self, cam_num):
        process_lst = []

        # 每个相机生成一个生产者 两个消费者
        for i in range(cam_num):
            process_lst.append(Capture(i))
            process_lst.append(Detect(i))
            process_lst.append(Detect(i))
        process_lst.append(Control_main(cam_num))

        for i in process_lst:
            i.start()
        for i in process_lst:
            i.join()

if __name__ == '__main__':
    from 常用模块 import redis_singleton
    RS = Redis_subscribe()
    Start_all(redis_singleton.config['cameras']['camNum'])



'''
from multiprocessing import Process,Queue,Lock
from threading import Thread
import random
import time


# lock = Lock()

class Capture(Process):
    def __init__(self, queue_dict, cam_id):
        super(Capture, self).__init__()
        self.cam_id = cam_id
        self.roi_queue = queue_dict['roi_queue_'+str(cam_id)]
        # self.singleton = GlobalSingleton()
        self.capt = False

    def capture(self):
        for item in self.singleton.subscribe().listen():
            if item['type'] == 'message' and item['data'] == '1':
                self.capt = True

    def run(self) -> None:
        count = 0
        # get_sub = Thread(target=self.capture, args=())
        # get_sub.setDaemon(True)
        # get_sub.start()

        while True:
            time.sleep(5)
            self.capt = True
            if self.capt:
                try:
                    roi = random.randint(0,4)
                    # print(roi)
                    self.roi_queue.put({'cam_id':self.cam_id, 'count':count, 'value':roi})
                    count += 1
                    self.capt = False
                except:
                    pass

class Detect(Process):
    def __init__(self, queue_dict, cam_id):
        super(Detect, self).__init__()
        self.cam_id = cam_id
        self.roi_queue = queue_dict['roi_queue_'+str(cam_id)]
        self.ret_queue = queue_dict['ret_queue_'+str(cam_id)]

    def run(self) -> None:
        while True:
            try:
                roi = self.roi_queue.get()
                roi['value'] = bool(roi['value'])
                self.ret_queue.put(roi)
                time.sleep(0.8)
            except:
                pass


class Control_main(Process):
    def __init__(self, queue_dict, cam_num):
        super(Control_main, self).__init__()
        self.ret_queue = []
        for key, value in queue_dict.items():
            if 'ret_queue_' in key:
                self.ret_queue.append(value)
        self.cam_num = cam_num
        self.part_lst = [None] * cam_num
        # self.redis_pub = GlobalSingleton()

    def cam_merge(self):
        try:
            for i in self.ret_queue:
                item = i.get()
                self.part_lst[item['cam_id']] = item['value']
                if item['cam_id'] == 0:
                    self.count = item['count'] - self.cam_num + 1 + 1
        except:
            pass

    def run(self) -> None:
        while True:
            # self.redis_pub.publish('1')
            lst_copy_1 = self.part_lst.copy()
            self.cam_merge()
            lst_copy_2 = self.part_lst.copy()
            for i in range(self.cam_num - 1):
                self.part_lst[i+1] = lst_copy_1[i] and lst_copy_2[i+1]

            if self.count < 1:
                print(None)
            else:
                print(self.count, self.part_lst[self.cam_num-1])



class Start_all(object):
    def __init__(self,cam_num):
        queue_dict = {}
        process_lst = []
        for i in range(cam_num):
            queue_dict['roi_queue_'+str(i)] = Queue()
            queue_dict['ret_queue_'+str(i)] = Queue()

        #每个相机生成一个生产者 两个消费者
        for i in range(cam_num):
            process_lst.append(Capture(queue_dict,i))
            process_lst.append(Detect(queue_dict,i))
            process_lst.append(Detect(queue_dict,i))
        process_lst.append(Control_main(queue_dict,cam_num))

        for i in process_lst:
            i.start()
        for i in process_lst:
            i.join()

if __name__ == '__main__':
    Start_all(3)
'''