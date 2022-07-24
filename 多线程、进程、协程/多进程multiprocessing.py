from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process
import time
import math

#多进程用于CPU密集型计算
PRIMES = [1122725350995293] * 100

def is_prime(n):
    if n <2:
        return False
    elif n ==2:
        return True
    if n%2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3,sqrt_n+1, 2):
        if n % i == 0:
            return False
    return True

#1 Process(target=is_prime, args=(i,))
def multi_process():
    multi_lst = [Process(target=is_prime, args=(i,)) for i in PRIMES]
    for i in multi_lst:
        i.start()
    for i in multi_lst:
        i.join()

#3 进程池      推荐  可控制开启进程数量上限
def multi_process_pool():
    with ProcessPoolExecutor() as pool:
        results = pool.map(is_prime, PRIMES)
        # for i in results:
        #     print(i)

#2 继承Process类
class Multi_Process_Class(Process):
    def __init__(self, n):
        super(Multi_Process_Class, self).__init__()
        self.n = n

    def is_prime(self):
        if self.n < 2:
            return False
        elif self.n == 2:
            return True
        if self.n % 2 == 0:
            return False
        sqrt_n = int(math.floor(math.sqrt(self.n)))
        for i in range(3, sqrt_n + 1, 2):
            if self.n % i == 0:
                return False
        return True

    def run(self):
        self.is_prime()


if __name__ == '__main__':
    start = time.time()
    multi_process()
    end = time.time()
    print('Time_Process = ', end - start, 'seconds')

    start = time.time()
    multi_process_pool()
    end = time.time()
    print('Time_Process_Pool = ', end - start, 'seconds')

    start = time.time()
    mutil_lst = [Multi_Process_Class(i) for i in PRIMES]
    for i in mutil_lst:
        i.start()
    for i in mutil_lst:
        i.join()
    end = time.time()
    print('Time_Process_Class = ', end - start, 'seconds')