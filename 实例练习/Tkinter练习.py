import tkinter as tk

#1
'''
class App:
    def __init__(self,master):
        frame=tk.Frame(master)          #Frame用于划分框架
        frame.pack(side=tk.BOTTOM,padx=10,pady=50)    #side=tk.LEFT 设置位置  padx距x轴距离
        self.hi_there=tk.Button(frame,text="打招呼",fg="yellow",bg='green',command=self.say_hi)   #commend=表示当按钮被按下时调用该函数  调用类内部的函数要加上self.
        self.hi_there.pack()

    def say_hi(self):
        print('你好')

root=tk.Tk()
root.title('打招呼')
root.geometry('500x300')
app=App(root)
'''
'''
#2
root=tk.Tk()
lst=[
    ('python',1),
    ('java',2),
    ('c++',3),
    ('ruby',4)]
v=tk.IntVar()
for i,j in lst:
    b=tk.Radiobutton(root,text=i,variable=v,value=j).pack(anchor=tk.W)
'''
#3
root=tk.Tk()
tk.Label(root,text='账号:').grid(row=0,column=0,padx=10,pady=5)
tk.Label(root,text='密码:').grid(row=1,column=0,padx=10,pady=5)
v1=tk.StringVar()
v2=tk.StringVar()
tk.Entry(root,textvariable=v1).grid(row=0,column=1,padx=10,pady=5)
tk.Entry(root,show='*',textvariable=v2).grid(row=1,column=1,padx=10,pady=5)
def show():
    print('账号:%s' % v1.get())
    print('密码:%s' % v2.get())
tk.Button(root,text='打印账号密码',command=show).grid(row=3,column=0,sticky=tk.W,padx=10,pady=5)
tk.Button(root,text='退出',command=root.quit).grid(row=3,column=1,sticky=tk.E,padx=10,pady=5)
root.mainloop()

