#获取指定目录下的所有Python文件
import os
path=os.getcwd()                     #getcwd（）获取文件路径（所在文件夹），无文件名
lst=os.listdir()
lst_1=os.listdir(path="../..")           #listdir()方法，获取文件夹下所有文件  ‘.’表示当前文件夹，'..'表示上一文件夹
print(path)
print(lst,'\n',lst_1)
for filename in lst:
    if filename.endswith(".py"):      #——.endswith()函数  判断是否以。。结尾
        print(filename,end='')
print()

#----用os.walk()遍历路径下的所有文件----
import os.path
import time

print("----用os.walk()遍历路径下的说有文件----")
path=os.getcwd()
lst_files=os.walk(path)
for dirpath,dirname,filename in lst_files:
    for dir in dirname:
        print(os.path.join(dirpath,dir))
    for file in filename:
        print(os.path.join(dirpath,file))

time_1=time.localtime(os.path.getctime('a.txt'))         #getctime 文件创建时间  getatime最后访问时间  getmtime最后修改时间
print(time_1)
print(time.strftime('%Y-%m-%d %H:%M:%S',time_1))        #time.strftime将时间以%Y-%m-%d %H:%M:%S格式字符串输出
