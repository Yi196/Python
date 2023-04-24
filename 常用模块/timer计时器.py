import time
from count_timer import CountTimer
from threading import Timer

''' 
CountTimer: 计时器可暂停、可恢复，计时器达到设定值后不会停止，会继续增加

Timer: 定时器达到设定值后调用回调函数，不可暂停，达到定时前可取消
'''


###################### CountTimer #######################
timer = CountTimer(10)   # 设置计时时间
print(timer.__dir__())

timer.start()            # 启动计时器

time.sleep(1.5)
# 查看
print(timer.elapsed)     # 当前计时时长
print(timer.duration)    # 计时器设置值
print(timer.remaining)   # 计时器剩余时长
print(timer.expired)     # 是否达到设定值
print(timer.paused)      # 是否暂停
print(timer.running)     # 是否正在运行


# 方法
timer.pause()            # 暂停计时器
timer.resume()           # 恢复暂停的计时器
timer.reset(10)          # 将计时器恢复到创建时的原始状态
print(timer.running)
print('########################')


###################### Timer #######################
def test(a):
    print(a)

tr = Timer(5, test, args=('111',))   # 5秒后执行test函数
tr.start()
# tr.join()   # 加入阻塞
print(22222)

# tr.cancel()  # 达到定时前可取消