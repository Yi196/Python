import asyncio  #实现异步I/O操作 使用async可以定义协程 协程用于耗时的io操作

#@asyncio.coroutine  Pyth3.4及以前版本使用修饰器将函数装饰为一个协程 3.4以后使用  async def
async def sleep(x):
    for i in range(3): # 协程函数
        print('sleep {}'.format(i))
        #yield from asyncio.sleep(1)  3.4之前版本使用yield from。。
        await asyncio.sleep(x)
    return "result = {}".format(1000)

# 事件循环
loop = asyncio.get_event_loop()

# 本质就是tasks的ensure_future,把协程包装进一个Future对象中,并使用create_task返回一个task
future1= asyncio.ensure_future(sleep(3))   #将协程包装成一个Future对象  因为通过Future对象可以了解任务执行的状态数据   事件循环来监控Future对象是否完成
#asyncio.ensure_future(coroutine) 和 loop.create_task(coroutine)都可以创建一个task
tasks=[future1,asyncio.ensure_future(sleep(1))]
#当有多个Future对象时,为了实现并发，要使用asyncio.wait(tasks)或 asyncio.gather(*tasks) ,前者接受一个task列表，后者接收一堆task。

# 内部会调用ensure_future,内部会执行loop.run_forever()
loop.run_until_complete(asyncio.wait(tasks))  #并行时当一个协程运行到阻塞程序时，会被挂起，主线控制权交给其他协程，直到其他协程挂起或执行完毕

print('-' * 30)
loop.close()
print(tasks[0].result()) # 拿return值,此处tasks是一个列表
print('===end===')
