import os
import json



def convert(json_path):
    save_dir = os.path.join(os.path.split(json_path)[0], 'result')
    os.makedirs(save_dir, exist_ok=True)
    with open(json_path, 'r', encoding='UTF-8') as f:
        value = json.loads(f.read())

    projects = value['projects']

    same_name_img = []
    count = 0
    for p in projects:
        print('projectId:', p['projectId'])
        tasks = p['tasks']
        for t in tasks:
            frames = t['frames']
            for f in frames:
                fileUrl = f['fileUrl']
                img_name = str(fileUrl).split('/')[-1]
                file_name = os.path.splitext(img_name)[0] + '.json'
                print(file_name)

                annotations = f['annotations']

                ret = {'label_box2D': []}
                if annotations:
                    ret['label_box2D'] = annotations['label_box2D']

                json_path = os.path.join(save_dir, file_name)
                if os.path.exists(json_path):
                    json_path = os.path.join(save_dir, str(img_name) + '.json')
                    same_name_img.append(img_name)
                with open(json_path, 'w') as f:
                    f.write(json.dumps(ret))
                count += 1

    print('同名文件为：', same_name_img)
    print('Done!')
    print('count:', count)





if __name__ == '__main__':
    from tkinter import filedialog
    # json_path = r'/home/mafneg/下载/003.json'
    json_path = filedialog.askopenfilename(title='select json file:', filetypes=[('json', '.json')])
    print(json_path)
    convert(json_path)