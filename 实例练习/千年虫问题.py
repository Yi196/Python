#千年虫  00 年在列表中存为 0  现将年份改为四位数存储
year=[89, 79, 65, 94, 67, 00, 7, 13]
print(enumerate(year))
for a1,b1  in enumerate(year):             #eumerate()函数返回一个包含原列表 索引和对应值的可迭代对象
    if int(b1)<10:
        year[a1]=int("200"+str(b1))
    elif 9<int(b1)<22:
        year[a1] = int("20" + str(b1))
    else:
        year[a1] = int("19" + str(b1))
print(year)


#猜数
import random
a=random.randint(0,100)       #产生一个随机数

for _ in range(1,11):
    b = int(input("请输入一个整数"))
    if b<a:
        print("小了")
    elif b>a:
        print("大了")
    elif b==a:
        print("猜对了")
        break
else:
    print("机会已用尽")

#逆向取值

lst=[0,1,2,3,4,5,6,7,8,9]
for i in range(len(lst)-1,-1,-1):  #逆向取值
    print(lst[i])


a=["asd","dasd","sad"]
print("|".join(a))
print("sadasd".find("as"))