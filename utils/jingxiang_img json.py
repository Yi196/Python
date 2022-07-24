import json
import os
import cv2


# 获取指定目录下后缀为suffix的所有文件名
# path为文件夹路径，suffix为后缀
def get_file_name(path, suffix):
    names = []
    file_list = os.listdir(path)  # 返回目录下的所有文件
    for file in file_list:

        split = os.path.splitext(file)  # 把文件名和后缀分开
        # 判断后缀是否相同
        if split[1] == suffix:
            names.append(split[0])

    return names

# src为json文件的地址，output为json文件输出地址，image_shape为图片的[height，width]，img_path为对应json文件的图片地址，item 镜像方式
def change_json(src, output, img_shape, img_path, item):
    try:
        with open(src,'r') as load_f:
            json_data = json.load(load_f)  # 加载json数据
            json_data['imagePath'] = img_path # 改变img的为对应的路径
            for point in json_data['shapes']:
                if item==-1 or item==0:
                    point['points'][0][1] = img_shape[0] - float(point['points'][0][1])
                    point['points'][1][1] = img_shape[0] - float(point['points'][1][1])
                if item==-1 or item==1:
                    point['points'][0][0] = img_shape[1] - float(point['points'][0][0])
                    point['points'][1][0] = img_shape[1] - float(point['points'][1][0])

            with open(output,'w') as new_file:
                new_file.truncate() #清空文件
                json.dump(json_data,new_file)
            new_file.close()
        load_f.close()

    except FileNotFoundError:
        print("%s is not found!" % src)
    except PermissionError:
        print("You don't have permission to access %s" % src)


def save_file(name, path, file_name, item):
    img_path = os.path.join(path, name + '.png')
    json_path = os.path.join(path, name + '.json')
    # 文件名最后一个字母为'_'的文件均为旋转后的图片
    json_output_path = os.path.join(path,name + file_name + '.json')
    img_output_path = os.path.join(path, name + file_name + '.png')
    img = cv2.imread(img_path)
    h,w,ch = img.shape

    img_changed = cv2.flip(img,item) # 镜像  item= -1 旋转180度  0 垂直镜像 1 水平镜像

    change_json(json_path, json_output_path, [h, w], name + file_name + '.png', item) # 改变旋转后的点并存储
    cv2.imwrite(img_output_path, img_changed) # 保存旋转后的图片


# 本函数是对图片进行    180度旋转        垂直镜像     水平镜像，并调整对应的json文件
def jingxiang(path, xuanzhuan=True, flit=False, mirror=False):
    # 获取图片文件名称
    img_names = get_file_name(path, ".png")
    for name in img_names:
        if xuanzhuan:
            save_file(name, path, file_name='_', item=-1)
        if flit:
            save_file(name, path, file_name='_f', item=0)
        if mirror:
            save_file(name, path, file_name='_m', item=1)


if __name__ == '__main__':
    # 传入文件夹路径，包含图片和对应的json文件
    path = 'C:/Users/dihuge/Desktop/000'
    #               xuanjuan:180度旋转 flit:垂直镜像  mirror:水平镜像
    jingxiang(path, xuanzhuan=True, flit=True, mirror=True)

