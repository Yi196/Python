with open ("test.txt","a+",encoding="utf-8") as file_1:
    print("奋斗成就更好明天！",file=file_1)    #用关键字file= 指定文件位置
    file_1.write("奋斗成就更好明天！")         #用io输入

with open ("test.txt","r",encoding="utf-8") as file_1:
    for item in file_1:                    #可直接遍历文件名，逐行输出文件内容
        print(item,end="")

#生成字典
lst1=["小明","小红","小兰"]
lst2=[78,45,87]
d={a:b for a,b in zip(lst1,lst2)}
print(d)
#遍历
for d1 in d:
    print(d1,d[d1])