import pickle  #将列表 字典 元组等Python结构转换成二进制存储，方便调用
dict={'xiaohong':29,'xiaoming':556,'xiaolan':54}
with open('134.txt','wb')as file:
    pickle.dump(dict,file)
with open('134.txt','rb')as file:
    print(pickle.load(file))
