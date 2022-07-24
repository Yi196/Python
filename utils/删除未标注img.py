import os.path
import easygui


def get_file_name(path, suffix):
    # 获取指定目录下后缀为suffix的所有文件名
    names = []
    file_list = os.listdir(path)  # 返回目录下的所有文件
    for file in file_list:

        split = os.path.splitext(file)  # 把文件名和后缀分开
        # 判断后缀是否相同
        if split[1] == suffix:
            names.append(split[0])

    return names


# 对于标注文件夹下的文件，未标注的文件从src中移动到dst中
# src原始文件路径，dst为目的文件路径
def move_file(src):
    json_files = get_file_name(src, ".json")  # 获取所有json文件名,不带后缀
    png_files = get_file_name(src, ".png")  # 获取所有png文件名，不带后缀

    diff_files = set(png_files).difference(set(json_files))  # 获取pngFiles与jsonFiles的差集，找出不同元素

    for file_Name in diff_files:
        file_path = os.path.join(src, file_Name + ".png")

        # 删除文件
        # 复制到指定文件夹
        # img_copy = os.path.join('C:/Users/Yi/Desktop/001', file_Name + ".png")
        # src_file = open(f"{file_path}", "rb")
        # copy_file = open(f"{img_copy}", "wb")
        # copy_file.write(src_file.read())
        # src_file.close()
        # copy_file.close()
        os.remove(file_path)


if __name__ == '__main__':
    src = easygui.diropenbox()  # 返回选择的文件夹
    move_file(src)
