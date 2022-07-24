def maxfactor(num):
    count=num//2+1
    while count>1:
        if num%count==0:
            print(f'{num}最大公约数为{count}。')
            break
        count-=1
    else:
        print(f"{num}为素数。")

if __name__ == '__main__':
    while True:
        try:
            num=int(input('请输入一个整数：'))
            maxfactor(num)
            break
        except:
            print('输入错误，请输入一个整数。')
