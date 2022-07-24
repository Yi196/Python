
import datetime
def inputdate():
    indata=input("请输入开始时间：（例如20210401按回车键结束）")
    indata=indata.strip()           #去除字符串两端的空格
    datestr=indata[0:4]+"-"+indata[4:6]+"-"+indata[6:]     #切片加上连接符-  形成2021-04-01形式
    return datetime.datetime.strptime(datestr,"%Y-%m-%d")  #将字符串转换为时间

if __name__ == '__main__':
    print("--------------推算时间-------------------")
    while True:
        try:
            sdate=inputdate()
            in_num=int(input("请输入间隔天数"))
            fdate = sdate + datetime.timedelta(days=in_num)
            break
        except:
            print("输入不正确请重新输入!")

    print("您推算的时间为：" + str(fdate))
    print("您推算的时间为："+str(fdate)[0:10])              #切片
    print("您推算的时间为：" + str(fdate).split(" ")[0])    #按空格分割成两部分的列表，取列表的第一个值