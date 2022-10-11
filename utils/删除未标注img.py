import os.path
import easygui

def remove_file(img_src, json_src):
    img_names = os.listdir(img_src)
    json_names = os.listdir(json_src)
    imgs = []
    jsons = []
    for file in img_names:
        imgs.append(os.path.splitext(file)[0])
    for file in json_names:
        jsons.append(os.path.splitext(file)[0])

    diff_files = set(imgs).difference(set(jsons))  # 获取img与json的差集，找出不同元素

    for file_Name in diff_files:
        for imgname in img_names:
            if file_Name in imgname:
                img = os.path.join(img_src, imgname)
                os.remove(img)
                # continue


if __name__ == '__main__':
    img_src = easygui.diropenbox(title='请选择图片地址')  # 返回选择的文件夹
    json_src = easygui.diropenbox(title='请选择json文件地址')
    remove_file(img_src, json_src)
