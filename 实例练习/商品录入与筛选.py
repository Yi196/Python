goods=[]
gcar=[]
while True:
    a=input("请输入商品编号 名称，一次输入一个商品，按\"q\"键停止输入")
    if a=="q":
        break
    else:
        goods.append(a)
goods_1=goods
while True:
    b=input("请输入要查找的商品名称或编号,按\"q\"结束")
    for item in goods_1:
        if item.find(b)!=-1:            #find()字符串查找 未找到返回-1
            gcar.append(item)
            goods_1.remove(item)        #remove()删除列表中第一次出现的item元素  此处为了避免重复查找
            break
        else:
            print("未找到该商品，请重新输入：")
            break
    if b=="q":
        break
print("你选择的商品为：")
for item in range(len(gcar)-1,-1,-1):            #逆向输出列表  也可直接逆向切片
    print(gcar[item])

#元组查找
d=(("广州",98),("成都",78),("武汉",67),("北京",56),("上海",65))

for index ,d1 in enumerate(d):
    print(str(index+1)+"、"+str(d1[0])+"  "+str(d1[1]))

for index ,d1 in enumerate(d):
    print(str(index+1)+"、",end="")
    for i in d1:
        print(str(i),end="")
    print()