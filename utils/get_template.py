import cv2, _pickle, time
import numpy as np
import os

def get_template(img, threshold, max_num_points, file_path):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('', binary)
    # cv2.waitKey(0)
    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    def _cont_area(cont):
        return cv2.contourArea(cont)

    contours.sort(key=_cont_area, reverse=True)
    points = contours[1]   # [[[x1,y1]],[[x2,y2]],...]

    number = points.shape[0]
    points_template = []

    # 降采样 限制模板中点的最大数量
    if number > max_num_points:
        for i in np.linspace(0, number - 1, max_num_points):
            i = int(i)
            points_template.append(points[i][0])
        number = max_num_points
    else:
        points_template = np.squeeze(points, 1)  # # [[x1,y1],[x2,y2],...]

    x_sum, y_sum = np.sum(points_template, 0)

    # 计算重心
    center_gravity_y = int(y_sum / number)
    center_gravity_x = int(x_sum / number)

    # 偏移重心
    for i in range(number):
        x, y = points_template[i]
        points_template[i] = [x - center_gravity_x, y - center_gravity_y]

    template = {}
    # 模板文件内存入信息
    template['points_number'] = number
    template['points'] = points_template
    template['center_gravity'] = [center_gravity_x, center_gravity_y]
    # print(template)
    _save_template(template, file_path)

    # 显示
    img_show = img.copy()
    for i, j in points_template:
        cv2.circle(img_show, (int(i + center_gravity_x), int(j + center_gravity_y)), 1, (0, 0, 255), -1)
        cv2.imshow('', img_show)
        cv2.waitKey(20)
    return True


def _save_template(template,file_path):
    with open(file_path,'wb') as file:
        _pickle.dump(template,file)


if __name__ == '__main__':
    dir = r'./template/'
    img_name = os.path.join(dir,'temp.png')
    file_path = os.path.join(dir,'template.pkl')
    img = cv2.imread(img_name)
    ret = get_template(img, 110, 32, file_path)
    print(ret)