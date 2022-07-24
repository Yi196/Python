#获取指定目录下的所有Python文件
import os
path=os.getcwd()
lst=os.listdir(path)
for filename in lst:
    if filename.endswith(".py"):     #——.endswith()函数  判断是否以。。结尾
        print(filename)
print()

import os.path
print("----用os.walk()遍历路径下的说有文件----")
path=os.getcwd()
lst_files=os.walk(path)
for dirpath,dirname,filename in lst_files:
    for dir in dirname:
        print(os.path.join(dirpath,dir))
    for file in filename:
        print(os.path.join(dirpath,file))