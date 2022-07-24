import time

print(time.localtime())    #输出当地时间
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))  #以%Y-%m-%d %H:%M:%S的格式输出时间

def show_info():
    try:
        while True:
            a=int(input("请输入以选择操作：0、退出；1、查看登录日志。0/1"))
            if a==1:
                read_logininfo()
                show_info()
                break
            elif a==0:
                break
            else:
                print("输入不正确，请重新输入。")
    except:
        print("请输入有效数字以选择操作")
        show_info()

def write_logininfo(username):
    with open("log.txt","a+",encoding="utf-8") as file:
        file.write(f"用户：{username},于{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}登录系统。\n")   #注意：双（单）引号内不能用双（单）引号，单双引号岔开使用

def read_logininfo():
    with open("log.txt","r",encoding="utf-8") as file:
        while True:          # lst=file.readlines()   for item in lst:  print(item)
            item = file.readline()
            if item!="":
                print(item,end="")   #取消自动换行，因为item中包含换行信息
            else:
                break

if __name__ == '__main__':
    while True:
        user_name=input("请输入用户名：")
        password=input("请输入密码：")
        if user_name=="admin" and password=="admin" or user_name=="user1" and password=="user1":
            write_logininfo(user_name)
            show_info()
            break
        else:
            print("账号或密码不正确，请重新输入")


