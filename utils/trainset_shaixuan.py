import os
import json
import tqdm

def shaixuan(path_images,path_josns,path_copy):
    for file in tqdm.tqdm(os.listdir(path_jsons)):
        if not file.endswith('.json'):
            continue
        json_path = os.path.join(path_josns, file)
        load_f = open(json_path, 'r')
        json_data = json.load(load_f)  # 加载json数据
        json_data = json_data['shapes']
        for item in json_data:
            if item['label']=='mozhou' or item['label']=='0':
            # if item['label']=='maosi' or item['label']=='1':
            # if item['label']=='queliao' or item['label']=='2':
            # if item['label']=='yashang' or item['label']=='3': # and abs(item['points'][0][0]-item['points'][1][0])*abs(item['points'][0][1]-item['points'][1][1]>50):
            # if item['label']=='yijiao' or item['label']=='4':
            # if item['label']=='zangwu' or item['label']=='5':
            # if item['label']=='huangjiaodai':
                name = os.path.splitext(file)[0]
                #复制图片
                img_path = os.path.join(path_images,name+'.png')
                img_copy = os.path.join(path_copy,name+'.png')
                src_file = open(f"{img_path}", "rb")
                copy_file = open(f"{img_copy}", "wb")
                copy_file.write(src_file.read())
                src_file.close()
                copy_file.close()
                #复制json文件
                load_f.close()
                json_copy = os.path.join(path_copy,file)
                src_file = open(f"{json_path}", "rb")
                copy_file = open(f"{json_copy}", "wb")
                copy_file.write(src_file.read())
                src_file.close()
                copy_file.close()
                #删训练集
                os.remove(json_path)
                os.remove(img_path)
                break
        else:
            load_f.close()



if __name__ == '__main__':
    path_images = r'C:\Users\dihuge\Desktop\data\train\images'
    path_jsons = r'C:\Users\dihuge\Desktop\data\train\jsons'
    path_copy = r'C:\Users\dihuge\Desktop\000'
    shaixuan(path_images,path_jsons,path_copy)