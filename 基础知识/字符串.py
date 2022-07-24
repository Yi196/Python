print("------查找------")
a="saj jkKds jkADSA hDjk"
print(a.find("ak"))    # 从左到右查找 未找到返回-1
print(a.rfind("jk"))   # 从右到左查找 未找到返回-1
print(a.index("jk"))   # 未找到报错
# print(a.rindex("ck"))  #未找到报错

print("\n\n------大小写转换------")
print(a.upper())
print(a.lower())
print(a.swapcase())
print(a.capitalize())
print(a.title())

print("\n\n------对齐------")
print(a.center(30))
print(a.center(30,"*"))
print(a.ljust(30,"%"))
print(a.rjust(30,"^"))
print(a.zfill(30))
print("-3.1415926".zfill(15))    #字符串为负数时，0补在负号后
print('  去除前后空格  '.strip())


print("\n\n------将字符串分割成列表------")
print(a.split())
print(a.rsplit(maxsplit=2))          #可用maxsplit= 指定分割次数
b="asd|sadsa|sadasd|da\s|das\dsa"
print(b.rsplit( sep="|"))             #可用 sep= 指定分割符
print(b.split(sep="|",maxsplit=2))

print("\n\n------判断------")
print("askjl12312___dasdl".isidentifier())  #全为标识符？ 字母数字下划线
print("sad,".isidentifier())
print("\n\t\r".isspace())                   #全为空字符？
print("张三asd".isalpha())                   #全为字母？ 汉字也是字母
print("1312四".isdecimal())                 #全为十进制数字？ 只有阿拉伯数字 汉字不是
print("1231三四".isnumeric())               #全为数字？   汉字 是
print("dsa123三".isalnum())                #全为数字和字母？

print("\n\n------替换------")
c="hello world python java python"
print(c)
print(c.replace("python","c++"))
print(c.replace("python","c++",1))

print("\n\n------合并------")             #  将全为字符串的列表元组 合并为一个字符串
lst=["asd","213,12.4","asd113"]
t=("asd","213,12.4","asd113")
print("|".join(lst))                  #用“|”将lst列表链接为一个字符串
print("".join(t))
print("*".join("python"))            #若链接字符串则将字符串才开  类似extend（）

print("\n\n------比较------")
d="apple"
e="appl"
print(d>e)
print(ord("易"))                      #ord（）取原始值unicode码
print(chr(26131))                     #chr（）取值

print("\n\n------切片------")         #同列表  注意步长为负数是倒序切片
f="Hello,Python"
print(f[:6])
print(f[::-1])
print(f[11:5:-1])

print("\n\n------格式化 精度------")
name="张三"
age=24
#1
print("我叫%s，今年%d岁"% (name,age))
#2
print("我叫{0}，今年{1}岁".format(name,age))
#3
print(f"我叫{name}，今年{age}岁")
a1=123.1234
print("%8.2f" % (a1))          #同C语言
print("{0:8.2f}".format(a1))

print("\n\n------编码 解码------")
s1="海内存知己，天涯共此时"
#编码
print(s1.encode(encoding="UTF-8"))
#解码
s1_1=s1.encode(encoding="UTF-8")        #中文编码  GBK 一个中文两个字节     UTF-8一中文三字节
print(s1_1.decode(encoding="UTF-8"))