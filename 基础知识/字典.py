a={"yi":20,"age":26}
for x,y in a.items():
    print(x,y)

b=dict(name="yi",age=28)
print(b)

c=dict()
print(c)

#查
print(a["age"])
print(b.get("name"))
print(a.get("name",404))  #当字典a中午无键“name”时，输出404

# 删除 清空 添加 修改
print("-------------删除 清空 添加 修改--------------")
scores={"张山":99,"李四":78,"王五":89}
print(scores)
print("王五" not in scores)
del scores["张山"]  #删除键名为。。的元组
print(scores)
scores.clear()
print(scores)
scores["老虎"]=100 #增
print(scores)
scores["老虎"]=98   #改
print(scores)


d={"张山":99,"李四":78,"王五":89}
keys=d.keys()
print(keys)
print(list(keys))
values=d.values()
print(values)
items=d.items()
print(items)
print(list(items))

#遍历
print("-------------遍历--------------")
e={"张山":99,"李四":78,"王五":89}
for item in e:
    print(item,end="\t")   #键的遍历
print()
for item in e:
    print(e[item],end="\t") #值的遍历
print()

#字典生成式
print("-------------字典生成式--------------")
aa=["xiaomin","xiaohong","xiaozhang"]
bb=[21,22,25,23,12]
cc={ aa_a : bb_b   for aa_a,bb_b in zip(aa,bb)  }
print(cc)

cc_c={ aa_a.upper() : bb_b   for aa_a,bb_b in zip(aa,bb)  }   #  ___ .pper（）表示输出大写字母
print(cc_c)

#合并字典
print("-------------合并字典--------------")
a={
    'a':1,
    'b':2,
    'c':3,
}

b={
    'd':4,
}
c=dict(a,**b)

print(c)
