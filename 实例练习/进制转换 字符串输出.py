def fun():
    num=int(input("输入一个整数"))
    print(num,"的二进制数为:",bin(num))     #bin(a)  返回a的二进制数  得到字符串类型
    print(str(num)+"的二进制数为:"+bin(num))  #   +   只能连接字符串格式
    print("----------用格式化字符串输出-----------")
    print("%d的二进制数为：%s" % (num,bin(num)))
    print("{0}的二进制数位{1}".format(num,bin(num)))
    print(f"{num}的二进制数为{bin(num)}")
    print("八进制数为："+str(oct(num))+"16进制数为："+hex(num))
    print()
    print("进制转换 bin（）   oct（）   hex（） 返回都为字符型")

    print("num不为空" if num else "num为空")

if __name__ == '__main__':
    while True:
        try:
            fun()
            break
        except:
            print("程序出错，请输入整数。")
    print("_"*30)  #输出30个下划线