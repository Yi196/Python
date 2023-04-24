import asyncio
import random
import time

'''
异步执行
async: 可将普通函数、生成器包装成异步函数、异步生成器
await: 可挂起自身协程，并等待另一个协程完成直到返回结果
'''


async def async_fun():
    return 1

# 直接调用不会返回结果，会返回一个协程coroutine对象
# print(async_fun())  # <coroutine object async_fun at 0x10124b2c0>

# 协程通过.send()方法驱动, 但直接调用会报错：StopIteration
# print(async_fun().send(None))


def get_ret(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as e:
        return e.value


print(get_ret(async_fun()))


# 在协程中，可以通过await挂起自身协程
async def await_coroutine():
    return await async_fun()   # await只能出现在通过async装饰的函数中

print(get_ret(await_coroutine()))


# eg
class Potato:
    @classmethod
    def make(cls, num, *args, **kwargs):
        potatos = []
        for i in range(num):
            potatos.append(cls.__new__(cls))
        return potatos

all_potatos = Potato.make(5)
# print(all_potatos)


async def ask_for_potato():
    await asyncio.sleep(random.random())     # 异步等待，会自动去执行其他协程，待其他协程完或挂起后才会继续执行
    all_potatos.extend(Potato.make(random.randint(1, 10)))


async def take_potatos(num):
    count = 0
    while True:
        if len(all_potatos) == 0:
            await ask_for_potato()

        potato = all_potatos.pop()
        yield potato

        count += 1
        if count == num:
            break


async def buy_potato():
    bucket = []
    async for p in take_potatos(50):
        bucket.append(p)
        print(f'Got one potato: {id(p)}')


async def buy_tomato():
    bucket = []
    async for p in take_potatos(30):
        bucket.append(p)
        print(f'Got one tomato: {id(p)}')


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # ret = loop.run_until_complete(buy_potato())
    # loop.close()

    print('#################异步执行###################')
    loop = asyncio.get_event_loop()
    ret = loop.run_until_complete(asyncio.wait([buy_potato(), buy_tomato()]))
    loop.close()
