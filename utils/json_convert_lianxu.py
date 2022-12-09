import os
import json
import re
import urllib
from flask import Flask

def convert(json_path):
    save_dir = os.path.join(os.path.split(json_path)[0], 'result')
    os.makedirs(save_dir, exist_ok=True)
    with open(json_path, 'r', encoding='UTF-8') as f:
        value = json.loads(f.read())

    projects = value['projects']

    same_name_img = []
    folder_name_lst = []
    for idx, p in enumerate(projects):
        print('projectId:', p['projectId'])
        tasks = p['tasks']
        folder_name = tasks[0]['frames'][0]['fileUrl']

        folder_name = [urllib.parse.unquote(i) for i in folder_name.split('/') if re.search(r'_\d+-\d+-\d+_\d+-\d+_', i)][0]
        print(folder_name)
        # folder_name = re.search(r'_\d+-\d+-\d+_\d+-\d+_', folder_name).group()
        if folder_name in folder_name_lst:
            folder_name = folder_name + f'___{idx + 1}'
        folder_name_lst.append(folder_name)
        print('folder_name: ', folder_name)
        img_dir = os.path.join(save_dir, folder_name)
        os.makedirs(img_dir, exist_ok=True)
        for t in tasks:
            frames = t['frames']
            for f in frames:
                fileUrl = f['fileUrl']
                img_name = str(fileUrl).split('/')[-1]
                file_name = os.path.splitext(img_name)[0] + '.json'
                print(file_name)

                annotations = f['annotations']
                ret = {}
                if annotations:
                    if annotations.get('label_box2DTrack', False):
                        ret = {'label_box2D': annotations['label_box2DTrack']}

                    elif annotations.get('label_polygon', False):
                        ret = {'label_polygon': annotations['label_polygon']}

                json_path = os.path.join(img_dir, file_name)
                if os.path.exists(json_path):
                    json_path = os.path.join(img_dir, str(img_name) + '.json')
                    same_name_img.append(json_path)
                with open(json_path, 'w') as f:
                    f.write(json.dumps(ret))

    print('同名文件为：', same_name_img)
    print('Done!')




if __name__ == '__main__':
    from tkinter import filedialog
    # json_path = r'/home/mafneg/下载/003.json'
    json_path = filedialog.askopenfilename(title='select json file:', filetypes=[('json', '.json')])
    print(json_path)
    convert(json_path)