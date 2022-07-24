import pickle  # 将列表 字典 元组等Python结构转换成二进制存储，方便调用
dict={'xiaohong':29,'xiaoming':556,'xiaolan':54}
with open(r'../基础知识/134.txt', 'wb')as file:
    pickle.dump(dict,file)     # 将要持久化的数据“对象”，保存到“文件”中
with open(r'../基础知识/134.txt', 'rb')as file:
    print(pickle.load(file))


import _pickle as plk  # python3 中用c语言重写了pickle  速度更快
a1 = [1,2,3,4,'000das']


b = plk.dumps(a1)  # 序列化单个对象  将obj对象序列化为string形式，而不是存入文件中

print(plk.loads(b))


import json

json_str = json.dumps(dict, indent=4)   # indent=4进行数据格式化输出
                                        #{
                                        #     "xiaohong": 29,
                                        #     "xiaoming": 556,
                                        #     "xiaolan": 54
                                        # }
str = json.loads(json_str)
print(str)