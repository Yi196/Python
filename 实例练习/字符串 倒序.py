a=[]
b=[]
with open("134.txt","r",encoding="utf-8") as file:
    a=file.read()
for item in range(len(a)-1,-1,-1):
    b.append(a[item])
a="".join(b)
with open ("134.txt","a+",encoding="utf-8") as file:
    file.write(str(a))

#忽略大小写统计  只能查单个字符
count=count_1=0
a1="asdashlsakjASJKLDHJKASDHhkljHDJKhdkjhkjJKDjkdjkKDASHJKDSAasdsaqweoigggqweiknnxcv,mcxzcpoueruoiylfcnjzvioer;l"
b1=input("请输入要查找的字符")
for i in a1:
    if i.upper()==b1 or i.lower()==b1:
        count+=1
print(f"{b1}共出现{count}次")
#查多字符
a1=a1.lower()
b1=b1.lower()
while True:
    if a1.find(b1)!=-1:
        count_1+=1
        a1=a1.replace(b1,"  ",1)
    else:
        break
print(f"{b1}共出现{count_1}次")

