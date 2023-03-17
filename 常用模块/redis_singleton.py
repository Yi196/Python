import redis
from multiprocessing import Queue


_DEPLOY = True
config = {
    'cameras':{
        'camNum' : 2
    },
    'redis_params':{
        'IP': '127.0.0.1',
        'port': 6379,
        'password': None,
        # 'password': 'dihuge' if _DEPLOY else 'rd_face18',
        'chan_sub': 'fm654'
    }
}


# 创建单例(生成类属性队列 或者实例属性队列 都能实现当某个实例改变队列地址时其他实例也跟着改变)
class Queue_Singleton(object):
    _instance = None
    __first_init = True
    # 根据相机数量创建队列
    names = locals()
    for i in range(config['cameras']['camNum']):
        names['roi_queue_' + str(i)] = Queue()
        names['ret_queue_' + str(i)] = Queue()
    # print(names)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self.__first_init:
            self.__first_init = False
            # self.queue_roi_0 = Queue()
            # self.queue_roi_1 = Queue()
            # self.queue_ret_0 = Queue()
            # self.queue_ret_1 = Queue()



class Redis_subscribe(object):
    def __init__(self):
        self.chan_sub = config['redis_params']['chan_sub']
        self.conn_redis()

    # 创建Redis数据库，写发布-订阅、存取数据 方法
    def publish(self, info):
        """
        发布消息
        将内容发布到频道
        """
        if self.redis_db is None:
            self.conn_redis()
        self.redis_db.publish(self.chan_sub, info)
        return True

    def subscribe(self):
        """
        订阅频道，配合多线程及
        for item in redis_sub.listen():
            if item['type'] == 'message':
                self.redis_sub = item['data']
        使用
        :return:
        """
        if self.redis_db is None:
            self.conn_redis()
        pub = self.redis_db.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub

    def set(self, *args, **kwargs):
        if self.redis_db is None:
            self.conn_redis()
        return self.redis_db.set(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.redis_db is None:
            self.conn_redis()
        return self.redis_db.get(*args, **kwargs)

    def conn_redis(self):
        self.redis_db = redis.Redis(
            connection_pool=redis.ConnectionPool(host=config['redis_params']['IP'],
                                                 password=config['redis_params']['password'],
                                                 port=config['redis_params']['port'],
                                                 decode_responses=True,
                                                 db=0))
        return self.redis_db



if __name__ == '__main__':
    from threading import Thread
    import time

    def get_redis_sub(redis_sub):
        for item in redis_sub.listen():    #item:{'pattern': None, 'type': 'message', 'channel': 'liao', 'data': '300033 1'}
            if item['type'] == 'message':
                print(item['data'])


    redis_bd = Redis_subscribe()

    # 开一个守护线程监听订阅的频道
    redis_sub = redis_bd.subscribe()
    get_sub = Thread(target=get_redis_sub, args=(redis_sub,))
    get_sub.setDaemon(True)
    get_sub.start()

    while True:
        print(redis_bd.get('002'))
        time.sleep(1)

"""
配合测试代码

import redis_singleton

redis_db = redis_singleton.Redis_subscribe()
redis_db.set('002','002nihaoya')
redis_db.publish('*****************522222')
print(redis_db.get('001'))
"""