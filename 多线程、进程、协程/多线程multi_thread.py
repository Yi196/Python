import blog_spider
import threading
import time

#多线程用于I/O密集型计算
def single_thread():      #单线程执行
    print('single_thread begin')
    for url in blog_spider.urls:
        blog_spider.craw(url)
    print('single_thread end')

def multi_thread():      #多线程执行
    print('multi_thread begin')
    threads = []
    for url in blog_spider.urls:
        threads.append(                                 #当参数daemon=True时，主线程结束后会关闭所有子线程
            threading.Thread(target=blog_spider.craw, args=(url,))     #定义多线程  target=函数名 args=（ 参数 ，）注意为元组
        )

    for thread in threads:
        # thread.setDaemon(True)  #设置守护线程，当程序中只剩下守护线程时程序会结束（如订阅Redis）
        thread.start()     #启动多线程

    for thread in threads:
        thread.join()     #Thread.join()方法，加入阻塞，等待对应线程执行结束后再继续执行主线程 可设定等待时间 秒
    print('multi_thread end')

if __name__ == '__main__':
    start=time.time()
    single_thread()
    end=time.time()
    print('Time = ',end-start,'seconds')

    start=time.time()
    multi_thread()
    end=time.time()
    print('Time = ',end-start,'seconds')