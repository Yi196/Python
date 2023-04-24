# -*- coding:utf8 -*-
import os
import cv2
import time
import ctypes
import numpy as np
from inference_onnx import MoveNet_onnx
from multiprocessing import sharedctypes
from torch.multiprocessing import spawn, Lock, Queue


'''
普通多进程会复制主进程的内存，导致模型的参数在子进程中无法被正确访问，使用torch.multiprocessing.spawn可开启多进程模型推理
Lock可添加进程锁
可配合共享内存等方式减小资源占用
'''

# python共享内存
'''
multiprocessing.Array 使用的是共享内存机制，是通过 mmap() 系统调用将一块内存映射到多个进程的虚拟地址空间中。而 multiprocessing.sharedctypes.Array 使用的是 ctypes 库，将数据缓存到一块公共内存区域中，不需要使用 mmap() 系统调用，而是使用操作系统提供的底层共享内存
multiprocessing.sharedctypes.Array 是 multiprocessing 模块提供的另一种共享内存类型，它是对 multiprocessing.Value 和 multiprocessing.Array 的底层封装，提供了更加简单易用的接口，并自动处理加锁和解锁的问题
multiprocessing.sharedctypes.RawArray 是一种基本的共享内存类型，它是 ctypes 库的一部分，可以用于在多个进程之间共享任何 ctypes 类型的数据。使用时需要手动控制加锁和解锁，因此使用起来较为繁琐。
multiprocessing.Manger 是通过共享进程实现内存共享
'''


class DetectMoveNet(object):
    def __init__(self, flag_bool, share_arr, queue):
        self.model = MoveNet_onnx(r'../weights/movenet_sim.onnx')
        self.flag = flag_bool
        self.arr = share_arr
        self.queue = queue
        print(self.queue)

    def run(self):
        while True:
            if self.flag[0]:
                # 将标志位至False
                self.flag[0] = False  # 先改标志位再赋值

                # 从共享内存中获取图片
                img = np.frombuffer(self.arr, dtype=np.uint8).reshape(1080, 1920, 3)
                print('get one img')

                kpt = self.model.detect(img, [0, 0, 9999, 9999])
                print(kpt.shape)
            else:
                time.sleep(0.1)

    def run2(self):
        while True:
            img = self.queue.get()
            kpt = self.model.detect(img, [0, 0, 9999, 9999])
            print('get one img')
            print(kpt.shape)


def run(rank, flag_bool, share_arr, queue):   # rank默认为进程编号，torch.multiprocessing.spawn 自动传入
    print('进程： ', rank)
    # DetectMoveNet(flag_bool, share_arr, queue).run()
    DetectMoveNet(flag_bool, share_arr, queue).run2()


# 使用共享内存，节省资源
def put_img(flag_bool, share_arr):
    count = 20
    while count:
        if not flag_bool[0]:
            frame = img.reshape(-1)
            temp = np.frombuffer(share_arr, dtype=np.uint8)
            temp[:] = frame

            flag_bool[0] = True  # 先赋值再改标志位
            print('put one img')

        else:
            time.sleep(0.1)

        count -= 1
        time.sleep(1)

# 使用队列，进程安全
def put_img2(queue):
    count = 20
    while count:
        queue.put(img)
        print('put one img')
        count -= 1
        time.sleep(1)

if __name__ == '__main__':
    import threading
    img = cv2.imread(r'../weights/test.jpg')
    img = cv2.resize(img, (1920, 1080))

    # # 创建共享内存
    # share_arr = sharedctypes.RawArray(ctypes.c_int8, 1080 * 1920 * 3)
    # # 设置标识位，或者使用进程锁
    # flag_bool = sharedctypes.RawArray(ctypes.c_bool, 1)
    #
    # threading.Thread(target=put_img, args=(flag_bool, share_arr,)).start()
    #
    # # args:传入参数，会自动在首位传入进程编号 nprocs:开启几个进程 join:阻塞  daemon:守护进程
    # spawn(run, args=(flag_bool, share_arr,), nprocs=2, join=True, daemon=True)



    q = Queue()
    threading.Thread(target=put_img2, args=(q,)).start()
    spawn(run, args=(None, None, q), nprocs=2, join=True)    # join 为False会报错，待解决。。。


    # mp.set_start_method('spawn', force=True)
    # p = mp.Process(target=producer, args=(queue, 10))