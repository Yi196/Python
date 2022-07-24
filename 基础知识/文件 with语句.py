# with语句 （又称上下文管理器）不管是否正常执行，都会退出文件，释放占用的资源
with open ("图片.png", "rb")as t1:
    with open("复制的图片.png", "wb")as t2:
        t2.write(t1.read())
# 不需要.close（）来关闭文件，跳出with语句时自动关闭
# 上下文管理器：实现__enter__()方法 __exit__()方法的类，及实现跳出自动释放资源的类对象就称为上下文管理器

with open ("a.txt", "r", encoding="utf-8") as file_1:
    lines = file_1.readlines()             # 将文件类容全部读入列表lines中，按行区分，可用lines[0].strip()去除换行符
    for item in file_1:                    # 可直接遍历文件名，逐行输出文件内容
        print(item,end="")

file=open("a.txt", "r", encoding="utf-8")    # 打开文件 “r/w/a/b/+”和encoding=utf-8”可省，默认为 r 和gbk 格式
print(file.readlines())                      # read()读取文件函数  readline（）读一行  readlines()按行形成一个列表
file.close()                                 # 关闭调用

file=open("a.txt", "a+", encoding="utf-8")
file.write("你好呀!")
lst=["12","123","13"]
file.writelines(lst)   # writelines（）将字符串列表写入文件
print(file.read())     # 此处无法显示文本内容，因为以追加形式打开的
file.close()

file=open("a.txt", "r", encoding="utf-8")
file.seek(3, 0)  # seek()文件指针向前移动3个位置，因utf-8三个字符一个汉字 若参数为负则向后移动指针
                 # 第二个参数：“0”从文件起始位置开始（默认），“1”从当前位置开始，“2”从文件末尾快开始
print(file.read())
print(file.tell())  # tell()返回文件指针位置
file.flush()        # 把缓冲区内容写入文件，但不关闭文件
file.close()

print("-------用rb/wb来复制图片 文件------")
src_file = open("图片.png", "rb")
copy_file = open("复制的图片.png", "wb")
copy_file.write(src_file.read())
src_file.close()
copy_file.close()