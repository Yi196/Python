def questio(question):
    c=0
    with open("test.txt","r",encoding="utf-8")as file:
        while True:
            lst={"付款","发货","退货"}
            a=(file.readline())
            if not a:
                break
            key1=a.split("|")[0]
            answer=a.split("|")[1]
            if key1 in question:
                lst=lst-{key1}         #强制将key1转换为集合，只能用{key1}
                print(key1+":"+answer,end="")
                print(f"您还可以咨询{str(list(lst)[0])+'、'+str(list(lst)[1])}等相关问题。")  #将集合先转为列表，在取列表内容转为字符
                c+=1
    if not c:
        return False
    else:
        return True

if __name__ == '__main__':
    while True:
        question=input("请输入您的问题：输入bye结束对话。")
        if question=="bye":
            break
        a=questio(question)
        if not a:
            print("我好像不明白，您可以咨询 支付 发货 退货 的相关问题。输入bye结束对话")
