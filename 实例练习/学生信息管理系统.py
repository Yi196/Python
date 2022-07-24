import os
import os.path
file="学生信息.txt"

def main():
    while True:
        menum()
        a=input("请选择操作:")
        if a.isdecimal():      #判断是否为数字串   也可用tyr： pass   except：  continue代替
            choice=int(a)
            if choice in [0,1,2,3,4,5,6,7]:
                if choice==0:
                    a1=input("您确定要退出吗？y/n")
                    if a1=="y"or a1=="Y":
                        print("感谢您的使用！")
                        break    #结束循环 退出系统
                    else:
                        continue
                elif choice==1:
                    insert()
                elif choice==2:
                    search()
                elif choice==3:
                    delete()
                elif choice==4:
                    modify()
                elif choice==5:
                    sort()
                elif choice==6:
                    total()
                else:
                    show()
            else:
                print("输入不正确，请输入0-7以选择操作！")
        else:
            print("输入不正确，请输入数字以选择操作！")

def menum():
    print("========================学生信息管理系统=========================")
    print("-------------------------- 功能菜单-----------------------------")
    print("\t\t\t\t\t\t1.录入学生信息")
    print("\t\t\t\t\t\t2.查找学生信息")
    print("\t\t\t\t\t\t3.删除学生信息")
    print("\t\t\t\t\t\t4.修改学生信息")
    print("\t\t\t\t\t\t5.排序")
    print("\t\t\t\t\t\t6.统计学生总人数")
    print("\t\t\t\t\t\t7.显示所有学生信息")
    print("\t\t\t\t\t\t0.退出")
    print("---------------------------------------------------------------")

def insert():
    student_lst=[]
    while True:
        id=input("请输入学生ID(如1001):")
        if not id:
            print("学生姓名、ID不能为空，请重新输入！")
            continue
        name=input("请输入学生姓名:")
        if not name:
            print("学生姓名、ID不能为空，请重新输入！")
            continue

        try:
            english=int(input("请输入英语成绩:"))
            python=int(input("请输入Python成绩:"))
            java=int(input("请输入Java成绩:"))
        except:
            print("输入无效，请输入数字！")
            continue
        student={"id":id,"name":name,"english":english,"python":python,"java":java}
        student_lst.append(student)   #把学生信息添加到列表中
        answer=input("是否继续添加？y/n")
        if answer=="y" or answer=="Y":
            continue
        else:
            break

    save(student_lst)   #调用save（）函数 将列表信息写入文件
    print("学生信息录入完毕！")
    student_lst.clear()

def save(student_lst):
    with open(file,"a+",encoding="utf-8")as file_1:
        for a2 in student_lst:
            file_1.write(str(a2)+"\n")    #将列表中的数据都转成str类型才能用write（）写入文件

def search():
    while True:
        if os.path.exists(file):
            with open(file,"r",encoding="utf-8")as file_1:
                student_lst=file_1.readlines()
            if student_lst==[]:
                print("未找到学生信息，请先录入。")
                break
            else:
                id1=""
                name1=""
                new_lst = []
                a=input("请选择查找方式：1、按学生ID查找；2、按学生姓名查找。1/2")
                if a=="1":
                    id1=input("请输入学生ID:(如1001)")
                elif a=="2":
                    name1=input("请输入学生姓名:")
                else:
                    print("输入不正确，请重新选择")
                    continue
                if id1=="":
                    for item1 in student_lst:
                        b2=dict(eval(item1))
                        if name1==b2.get("name"):
                            new_lst.append(b2)
                else:
                    for item2 in student_lst:
                        b2=dict(eval(item2))
                        if id1==b2.get("id"):
                            new_lst.append(b2)
                if new_lst==[]:
                    print("未找到相关信息！")
                else:
                    print("查找成功！结果如下:")
                    show_search(new_lst)
                    new_lst.clear()
                a3=input("是否继续查找？y/n:")
                if a3=="y" or a3=="Y":
                    continue
                else:
                    break
        else:
            print("未找到学生信息，请先录入。")
            break

def show_search(lst):
    title="{0:^10}\t{1:^12}\t{2:^12}\t{3:^12}\t{4:^12}\t{5:^12}\t"
    print(title.format("ID","姓名","英语成绩","Python成绩","Java成绩","总成绩"))
    data="{0:^10}\t{1:^12}\t{2:^12}\t{3:^12}\t{4:^13}\t{5:^14}\t"
    for a in lst:
        print(data.format(a.get("id"),a.get("name"),a.get("english"),a.get("python"),a.get("java"),
                          int(a.get("english"))+int(a.get("python"))+int(a.get("java"))))

def delete():
    while True:
        if os.path.exists(file):
            with open(file,"r",encoding="utf-8")as file_1:
                student_lst=file_1.readlines()
            if student_lst==[]:
                print("未找到学生信息，请先录入。")
                break
            else:
                biaozhiwei=False       #判断是否删除成功
                new_lst=[]
                a1 = input("请输入要删除的学生ID:")
                for b1 in student_lst:
                    b2=dict(eval(b1))      #将字符串转换为字典 eval（）函数作用  去掉字符串最外侧引号
                    if a1==b2.get("id"):
                        biaozhiwei=True
                        continue
                    else:
                        new_lst.append(b2)
                if biaozhiwei==True:
                    print(f"已成功删除ID为{a1}的学生信息。")
                else:
                    print(f"未找到ID为{a1}的学生信息。")
                with open(file, "w", encoding="utf-8")as file_1:
                    for a2 in new_lst:
                        file_1.write(str(a2)+"\n")
                a3=input("是否继续删除？y/n:")
                if a3=="y" or a3=="Y":
                    continue
                else:
                    break
        else:
            print("未找到学生信息，请先录入。")
            break

def modify():
    while True:
        if os.path.exists(file):
            with open(file,"r",encoding="utf-8")as file_1:
                student_lst=file_1.readlines()
            if student_lst==[]:
                print("未找到学生信息，请先录入。")
                break
            else:
                biaozhiwei=False       #判断是否修改成功
                new_lst=[]
                a1 = input("请输入要修改的学生ID:")
                for b1 in student_lst:
                    b2=dict(eval(b1))      #将字符串转换为字典 eval（）函数作用  去掉字符串最外侧引号
                    if a1==b2.get("id"):
                        biaozhiwei=True
                        while True:        #输入修改值
                            name = input("请输入学生姓名:")
                            if not name:
                                print("学生姓名、ID不能为空，请重新输入！")
                                continue

                            try:
                                english = int(input("请输入英语成绩:"))
                                python = int(input("请输入Python成绩:"))
                                java = int(input("请输入Java成绩:"))
                            except:
                                print("输入无效，请输入数字！")
                                continue
                            student = {"id": a1, "name": name, "english": english, "python": python, "java": java}
                            new_lst.append(student)
                            break
                    else:
                        new_lst.append(b2)
                if biaozhiwei==True:
                    print(f"已成功修改ID为{a1}的学生信息。")
                else:
                    print(f"未找到ID为{a1}的学生信息。")
                with open(file, "w", encoding="utf-8")as file_1:
                    for a2 in new_lst:
                        file_1.write(str(a2)+"\n")
                a3=input("是否继续修改？y/n:")
                if a3=="y" or a3=="Y":
                    continue
                else:
                    break
        else:
            print("未找到学生信息，请先录入。")
            break

def sort():
    if os.path.exists(file):
        lst_1=[]
        with open(file,"r",encoding="utf-8")as file_1:
            lst=file_1.readlines()
        if lst==[]:
            print("暂未保存数据。。。")
        else:
            for item in lst:
                a = dict(eval(item))
                lst_1.append(a)
            show_search(lst_1)
    else:
        print("暂未保存数据。。。")
    a1=input("请选择（1、升序；2降序）排序：1/2")
    if a1=="1":
        modle=False
    elif a1=="2":
        modle=True
    else:
        print("您的输入有误，请重新选择！")
        sort()
        return
    a2=input("请选择（0、按总成绩；1、按英语成绩；2、按Python成绩；3、按Java成绩）排序：0/1/2/3")
    if a2=="0":
        lst_1.sort(key=lambda x: int(x["english"])+int(x["python"])+int(x["java"]),reverse=modle)
        show_search(lst_1)
    elif a2=="1":
        lst_1.sort(key=lambda x: int(x["english"]), reverse=modle)
        show_search(lst_1)
    elif a2=="2":
        lst_1.sort(key=lambda x: int(x["python"]), reverse=modle)
        show_search(lst_1)
    elif a2=="3":
        lst_1.sort(key=lambda x: int(x["java"]), reverse=modle)
        show_search(lst_1)
    else:
        print("您的输入有误，请重新选择！")
        sort()
        return
    with open(file, "w", encoding="utf-8")as file_1:
        for a3 in lst_1:
            file_1.write(str(a3) + "\n")

def total():
    if os.path.exists(file):
        with open(file,"r",encoding="utf-8")as file_1:
            lst=file_1.readlines()
        if lst==[]:
            print("暂未保存数据。。。")
        else:
            print("一共有"+str(len(lst))+"位学生")
    else:
        print("暂未保存数据。。。")

def show():
    if os.path.exists(file):
        lst_1=[]
        with open(file,"r",encoding="utf-8")as file_1:
            lst=file_1.readlines()
        if lst==[]:
            print("暂未保存数据。。。")
        else:
            for item in lst:
                a=dict(eval(item))
                lst_1.append(a)
            show_search(lst_1)
    else:
        print("暂未保存数据。。。")

if __name__ == '__main__':
    main()                     #此语句必须在main（）函数下方，否者显示函数未定义