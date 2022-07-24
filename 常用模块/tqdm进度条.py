import time
from tqdm import tqdm, trange

# 进度条工具（可展示循环过程中可迭代序列的进度）
for i in tqdm(range(100),desc='这是一个进度条左侧说明'):
    time.sleep(0.02)

# 针对迭代对象是 range() 的情况，tqdm 还提供了简化版的 trange() 来代替tqdm(range())
temp = [time.sleep(0.02) for i in trange(100)]


# 手动更新描述
pbar = tqdm(range(100))
for i in pbar:
    pbar.set_description('Processing ' + str(i))
    time.sleep(0.02)



# #  配合 jupyter notebook/jupyter lab 的美观进度条 配合pandas中的apply
# from tqdm.notebook import trange,tqdm
# for i in trange(100):
#     time.sleep(0.02)


#  alive-progress 常用方法
# 但alive-progress相比tqdm增加了更多花样繁多的动态效果，我们通过调用其专门提供的showtime()函数可以查看所有可用的动态
import alive_progress
with alive_progress.alive_bar(10) as bar:
    for i in range(10):
        time.sleep(0.1)
        bar()