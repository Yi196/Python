import tkinter as tk
from PIL import Image, ImageTk
#标签
window=tk.Tk()    #创建窗口
window.title('My Window')   #标题
window.geometry('800x800')  #设置窗口大小  小写x
frame1=tk.Frame(window,bg='blue',width=400,height=400).pack(side='right')

tk.Label(frame1,text='你好！\nThis is Tinter',justify=tk.LEFT,padx=10,fg='yellow',bg='green',font=('Arial',12),width=30,height=2).pack(anchor=tk.W)
#Label()方法用于创建一个标签，justify 表示左对齐 fg前景色 bg为背景色，font为字体 width为长 height为高  这里的长和高是字符的长和高，比如height=2就表示标签有两个字符的高度
  #放置标签，自动调节 ：1）l.pack()  side设置在窗口中位置，anchor设置在框架中位置; 2)l.place();3)l.grid() 以表格形式布局设置好行列row= column=

#设置可变字符串           tk.StringVar（）  用set（）来设置
var=tk.StringVar()   # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
var.set('')

#图片
photo = ImageTk.PhotoImage(file=r'./OpenCV/image/003.jpg')  #tkinter 只能传如gif图片  故此处用PIL
image_lable=tk.Label(frame1,text='你好呀',image=photo,compound=tk.CENTER,font=('华康少女',20),fg='grey').pack(anchor=tk.W)      #compound=tk.CENTER 表示文字在图片上放
tk.Label(frame1, textvariable=var,bg='green', fg='white', font=('Arial', 12), width=30, height=2).pack(anchor=tk.W)    # 说明： textvariable表示可变字符串，他要通过tk.StringVar()定义  ，并用tk.set()设置内容
on_hit=False
def hit_me():
    global on_hit
    if on_hit==False:
        on_hit=True
        var.set('you touch me')
    else:
        on_hit=False
        var.set('')

#Button按钮   因为Python的执行顺序是从上往下，所以函数一定要放在按钮的上面
tk.Button(frame1,text='touch me',font=('Arial', 12),width=10,height=1,command=hit_me).pack(anchor=tk.W) #command指定按钮被按下时调用的函数名  这里的函数名后不加括号，若加括号表示不按按键直接调用函数

#CheckButton代表一个变量，它有两个不同的值。点击这个按钮将会在这两个值间切换
v1=tk.IntVar()
tk.Checkbutton(frame1,text="测试",variable=v1).pack(anchor=tk.W) #variable表示按键状态，选中为1

#Radiobutton代表一个变量，它可以有多个值中的一个。点击它将为这个变量设置值
v2=tk.IntVar()
tk.Radiobutton(frame1,text='one',variable=v2,value=1).pack(anchor=tk.W)   #每次选中按钮时，会把value的值赋给v2（variable）
tk.Radiobutton(frame1,text='two',variable=v2,value=2).pack(anchor=tk.W)   #anchor=tk.W表示左对齐

#Entry是tkinter类中提供的的一个单行文本输入域
e1 = tk.Entry(frame1, show='*', font=('Arial', 14)).pack(anchor=tk.W)  # show='*',显示成密文形式
e2 = tk.Entry(frame1, show=None, font=('Arial', 14)).pack(anchor=tk.W)  # 显示成明文形式

#Text是tkinter类中提供的的一个多行文本区域，显示多行文本，可用来收集(或显示)用户输入的文字(
t = tk.Text(frame1, height=3).pack(anchor=tk.W)

#
window.mainloop()  #主窗口循环显示k