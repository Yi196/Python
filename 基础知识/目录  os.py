import os

print(os.getpid())  # 获取进程ID
os.system("notepad.exe")  # 调用系统命令  打开记事本 类似win+r
os.system("calc.exe")
# os.startfile("E:\\QQ和微信\\Bin\\qq.exe")  #调用可执行文件 打开QQ

# 对目录的操作
print(os.getcwd())          # 返回当前操作目录
lst=os.listdir("..")        # 返回指定路径下的文件和目录信息  缺省为当前路经
print(lst)
lst1=os.walk(os.getcwd())   # 递归遍历路径上所有文件 包括子文件
os.mkdir("a1")              # 创建目录
os.makedirs("a2/a3/a4")     # 创建多级目录
os.rmdir("a1")              # 删除目录
os.removedirs("a2/a3/a4")   # 删除多级目录
os.chdir("../../")          # 将。。设为当前工作目录  "../" 表示放回上一级
print()

#os.path 模块
import os.path
print(os.path.abspath("字符串.py"))                                                 # 获取绝对路径
print(os.path.exists("字符串.py"), os.path.exists("123.txt"))                       # 判断文件是否存在
print(os.path.join(r"C:/Users/YJL/Desktop/Python练习/package", "134.txt"))          # 连接目录和文件
print(os.path.splitext(r"C:/Users/YJL/Desktop/Python练习/package/134.txt"))         # 分离拓展名
print(os.path.split(r"C:/Users/YJL/Desktop/Python练习/package/134.txt"))            # 分离路径和文件名
print(os.path.splitext("134.txt"))                                                 # 分离拓展名   和文件名或路径
print(os.path.splitext(r"C:/Users/YJL/Desktop/Python练习/package/134.txt"))         # 分离拓展名
print(os.path.basename(r"C:/Users/YJL/Desktop/Python练习/package/134.txt"))         # 提取文件名
print(os.path.dirname(r"C:/Users/YJL/Desktop/Python练习/package/134.txt"))          # 提取路径，不包含文件名
print(os.path.isdir(r"C:/Users/YJL/Desktop/Python练习/package/134.txt"))             # 判断是否为路径