from easygui import *
msgbox("你好",'标题','好的','Cat.png')   #msgbox(对话信息，标题，按钮文字，图片，root)
passwordbox("123")
buttonbox('这是模块？','Guess',choices=['shi','bushi'],image='Cat.png')
diropenbox()  #返回选择的文件夹
multenterbox(msg='输入以下内容', title='标题', fields=['姓名', '学号','金额'], values=[' ',' ',' '])

#https://blog.csdn.net/mingqi1996/article/details/81272621?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-8.control&dist_request_id=1328769.30577.16174656918191805&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-8.control
