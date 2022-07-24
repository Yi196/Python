from concurrent.futures import ThreadPoolExecutor, as_completed
import blog_spider
import time

#线程池可查看各线程的返回值
# 1
with ThreadPoolExecutor() as pool:
    results = pool.map(blog_spider.craw, blog_spider.urls)
    # 返回结果顺序与urls一致
    for result in results:
        print(result)

#2
with ThreadPoolExecutor() as pool:
    futures = [pool.submit(blog_spider.craw, url) for url in blog_spider.urls ]
    # 01返回结果顺序与urls一致
    for future in futures:
        print(future.result())
    # 02先执行完的线程结果优先显示
    for future in as_completed(futures):
        print(future.result())

#3
pool = ThreadPoolExecutor()

def aa1():
    time.sleep(0.1)
    return 'a1 result'
def aa2():
    time.sleep(0.2)
    return 'a2 result'
def aa3():
    time.sleep(0.3)
    return 'a3 result'

def bb():
    a1 = pool.submit(aa1)
    a2 = pool.submit(aa2)
    a3 = pool.submit(aa3)
    return {'a1':a1.result(),
            'a2':a2.result(),
            'a3':a3.result()}

if __name__ == '__main__':
    start = time.time()
    b = bb()
    print(b)
    end = time.time()
    print('Time = ', end - start, 'seconds')