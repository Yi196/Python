import numpy as np
import cv2
import os
from PIL import Image,ImageDraw,ImageFont
import easygui

def and_photo(path, path_long, length=500, width=600, str=None):

#合并长图
    name = os.listdir(path)
    path_long = os.path.join(path_long, 'img_long.png')
    for item in name:
        item = os.path.join(path,item)

        try:
            img =  cv2.imdecode(np.fromfile(item,dtype=np.uint8),-1)
            try:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            except:
                pass
            img_short = cv2.resize(img, (length, width))

        except:
            continue

        if not os.path.exists(path_long):
            cv2.imwrite(path_long,img_short)
        else:
            img_long = cv2.imread(path_long)

            img_long = np.concatenate((img_long,img_short),axis=0)
            cv2.imwrite(path_long, img_long)


#添加文字
    img = cv2.imread(path_long)
    h ,w = img.shape[:2]
    # print(h,w)
    # font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    # cv2.putText(img,'ok',(5,h-400), font, 3,(0,255,0) )  #不能添加中文

    pil_img = Image.open(path_long )
    # pil_img.show()
    # 生成画笔
    draw = ImageDraw.Draw(pil_img)
    # 第一个参数是字体文件的路径，第二个是字体大小
    font = ImageFont.truetype('simhei.ttf', 20, encoding='utf-8')
    # 第一个参数是文字的起始坐标，第二个需要输出的文字，第三个是字体颜色，第四个是字体类型
    draw.text((30, h-50), str, (0, 255, 255), font=font)

    # PIL图片转cv2
    cv2_text_im = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    cv2.imwrite(path_long,cv2_text_im)



if __name__ == '__main__':
    path = easygui.diropenbox(msg='请选择需要合并的图片所在文件夹：')
    path_long = easygui.diropenbox(msg='请选择合并后图片保存地址（应与刚刚地址不同）：')
    a,b,c = easygui.multenterbox(msg='输入以下内容', title='拼接长图', fields=['小图长', '小图宽','图片底部添加文字'], values=['500','600',''])
    length = int(a)
    width = int(b)
    str = c

    and_photo(path, path_long, length, width, str)