import random, time, os
import threading
import types
import ctypes
import multiprocessing
from multiprocessing import Queue, Value, Pipe, Array


# 多线程间通信 global
x = 10
def aa1():
    global x
    while True:
        x = random.random()
        time.sleep(0.5)

# threading.Thread(target=aa1, args=()).start()
# while True:
#     print(x)
#     time.sleep(0.3)


# *****************************************************
# 多进程间通信
# 1、队列Queue
queue_1 = Queue()
queue_1.qsize()  # 返回队列的大致长度。由于多线程或者多进程的上下文，这个数字是不可靠的
queue_1.empty()
queue_1.full()
# put(obj[, block[, timeout]])
# put_nowait(obj)   # 相当于 put(obj, False)
# get([block[, timeout]])
# get_nowait()      #相当于 get(False)
queue_1.put('001')
queue_1.get()
'''如果可选参数 block 是 True (默认值) 而且 timeout 是 None (默认值), 将会阻塞当前进程，直到能够存或取。
如果 timeout 是正数，将会在阻塞了最多 timeout 秒之后还是没有可用对象时抛出 queue.Full/queue.Empty 异常。
反之 (block 是 False 时)，仅当队列可用时返回，否则抛出 queue.Full/queue.Empty 异常 (在这种情形下 timeout 参数会被忽略)。
'''


# 2、管道Pipe
# Pipe() 返回一对 Connection对象 (conn1, conn2) ， 分别表示管道的两端。默认管道是双向的，并无先后之分，只要两个进程各持一段就可以
# 创建:multiprocessing.Pipe([duplex])  如果 duplex 被置为 True (默认值)，那么该管道是双向的。如果 duplex 被置为 False ，那么该管道是单向的，即 conn1 只能用于接收消息，而 conn2 仅能用于发送消息
pipe_1 = Pipe()
# pipe_1.send('obj')  # 发送
# pipe_1.recv()       # 接收


def proc_send(pipe, urls):
    for url in urls:
        print("Process (%s) send: %s" % (os.getpid(), url))
        pipe.send(url)
        time.sleep(random.random())


def proc_recv(pipe):
    while True:
        print("Process (%s) rev: %s" % (os.getpid(), pipe.recv()))
        time.sleep(random.random())


if __name__ == '__main__':
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=proc_send, args=(pipe[0], ['url_' + str(i) for i in range(10)]))
    p2 = multiprocessing.Process(target=proc_recv, args=(pipe[1],))
    p1.start()
    p2.start()


# 3、共享内存Value 或 Array  (数据操作最快)
def aa2(num, arr):
    num.value = 3.1415926535
    for i in range(len(arr)):
        arr[i] = -arr[i]
        time.sleep(0.8)

if __name__ == '__main__':
    num = Value(ctypes.c_double, 0.0)  #线程不安全
    arr = Array('f', range(10))
    # print(arr)
    multiprocessing.Process(target=aa2, args=(num, arr)).start()
    while True:
        print(num.value)
        print(arr[:])
        time.sleep(0.5)

# 4、共享进程Manger() 是线程安全的(Value、Array、dict、list、Lock、Semaphore、还可以共享类的实例对象等)
def aa2(share_value, share_lst, share_dict):
    while True:
        i = random.randint(0,4)
        share_value.value = i
        share_lst[i] = i
        share_dict[1] = f'{i}'
        time.sleep(1)

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    bool_data = manager.Value(ctypes.c_bool, False)   # Bool值
    int_data = manager.Value(ctypes.c_int, 0)         # 整型
    str_data = manager.Value(ctypes.c_char_p, 'str0') # 字符串

    list_data = manager.list([0, 0, 0, 0, 0])         # 列表
    dict_data = manager.dict()                        # 字典
    array_data = manager.Array('i', range(10))        # 数组
    lock = manager.Lock()

    multiprocessing.Process(target=aa2, args=(int_data, list_data, dict_data)).start()
    while True:
        print(int_data.value)
        print(list_data)
        print(dict_data)
        time.sleep(0.5)