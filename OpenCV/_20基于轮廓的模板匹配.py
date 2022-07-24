import cv2
import numpy as np
import _pickle


# 第一步，先提取边缘轮廓,并生成模板文件
# 计算梯度
def _gen_magnitude(img, angle=False):
    sobel_dx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    sobel_dy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    magnitude = cv2.magnitude(sobel_dx, sobel_dy)
    sobel_ag = None
    if angle:
        sobel_ag = cv2.phase(sobel_dx, sobel_dy, angleInDegrees=True)

        # 从0,45,90,135得到最近的角
        sobel_ag[np.where(((sobel_ag > 22.5) & (sobel_ag < 67.5)) | ((sobel_ag > 202.5) & (sobel_ag < 247.5)))] = 45
        sobel_ag[np.where(((sobel_ag > 67.5) & (sobel_ag < 112.5)) | ((sobel_ag > 247.5) & (sobel_ag < 292.5)))] = 90
        sobel_ag[np.where(((sobel_ag > 112.5) & (sobel_ag < 157.5)) | ((sobel_ag > 292.5) & (sobel_ag < 337.5)))] = 135
        sobel_ag[np.where((sobel_ag != 0 ) & (sobel_ag != 45) & (sobel_ag != 90) & (sobel_ag != 135))] = 0

    return sobel_dx, sobel_dy, magnitude, sobel_ag

# 非极大值抑制(按边缘 取边缘上两像素的最大值)
def _nms(magnitude, sobel_ag):
    h, w = magnitude.shape
    min_val,max_val,min_indx,max_indx= cv2.minMaxLoc(magnitude)
    nms_edges = np.zeros_like(magnitude)
    for i in range(1,h-1):
        for j in range(1,w-1):
            if sobel_ag[i,j] == 0:
                leftPixel = magnitude[i][j - 1]
                rightPixel = magnitude[i][j + 1]
            elif sobel_ag[i,j] == 45:
                leftPixel = magnitude[i - 1][j + 1]
                rightPixel = magnitude[i + 1][j - 1]
            elif sobel_ag[i,j] == 90:
                leftPixel = magnitude[i - 1][j]
                rightPixel = magnitude[i + 1][j]
            elif sobel_ag[i,j] == 135:
                leftPixel = magnitude[i - 1][j - 1]
                rightPixel = magnitude[i + 1][j + 1]

            if (magnitude[i][j] < leftPixel) or (magnitude[i][j] < rightPixel):
                nms_edges[i][j] = 0
            else:
                nms_edges[i][j] = int(magnitude[i][j] / max_val * 255)
    return nms_edges

# 做滞后阈值
def _double_threshold(nms_edges, max_threshold, min_threshold):
    h, w = nms_edges.shape
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if nms_edges[i,j] < max_threshold:
                if nms_edges[i,j] < min_threshold:
                    nms_edges[i,j] = 0
                else:  # 如果8个相邻像素中的任何一个不大于maxContrast，则从边缘中删除
                    if float(nms_edges[i - 1][j - 1]) < max_threshold and \
                        float(nms_edges[i - 1][j]) < max_threshold and \
                        float(nms_edges[i - 1][j + 1]) < max_threshold and \
                        float(nms_edges[i][j - 1]) < max_threshold and \
                        float(nms_edges[i][j + 1]) < max_threshold and \
                        float(nms_edges[i + 1][j - 1]) < max_threshold and \
                        float(nms_edges[i + 1][j]) < max_threshold and \
                        float(nms_edges[i + 1][j + 1]) < max_threshold:

                        nms_edges[i][j] = 0
    return nms_edges

# 将所选边缘的X和Y导数与坐标信息一起保存为模板模型
def _get_template(sobel_dx, sobel_dy, magnitude, nms_edges, max_num_points):
    template = {}
    points = np.where(nms_edges > 0)
    points = np.transpose(points) # [[y1,x1],[y2,x2],..]
    points_template = []
    gradient_y = []
    gradient_x = []
    magnit = []
    y_sum = 0
    x_sum = 0
    number = 0
    for y,x in points:
        if sobel_dy[y,x] != 0 or sobel_dx[y,x] != 0:
            y_sum += y
            x_sum += x
            points_template.append([y,x])
            gradient_y.append(sobel_dy[y,x])
            gradient_x.append(sobel_dx[y,x])
            if magnitude[y,x] != 0:
                magnit.append(1 / magnitude[y,x])
            else:
                magnit.append(0)
            number += 1

    # 计算重心
    center_gravity_y = int(y_sum / number)
    center_gravity_x = int(x_sum / number)

    # 偏移重心
    for i in range(number):
        y, x = points_template[i]
        points_template[i] = [y - center_gravity_y, x - center_gravity_x]

    # 降采样 限制模板中点的最大数量
    if number > max_num_points:
        points_t = []
        grad_y = []
        grad_x = []
        mg = []
        for i in np.linspace(0, number-1, max_num_points):
            i = int(i)
            points_t.append(points_template[i])
            grad_y.append(gradient_y[i])
            grad_x.append(gradient_x[i])
            mg.append(magnit[i])
        number = max_num_points
        points_template = points_t
        gradient_y = grad_y
        gradient_x = grad_x
        magnit = mg

    # 模板文件内存入信息
    template['points_number'] = number
    template['points'] = points_template
    template['gradient_y'] = gradient_y
    template['gradient_x'] = gradient_x
    template['magnitude'] = magnit
    template['center_gravity'] = [center_gravity_y,center_gravity_x]
    # print(template)
    return template

def _save_template(template,file_path):
    with open(file_path,'wb') as file:
        _pickle.dump(template,file)

def _read_template(file_path):
    with open(file_path,'rb') as file:
        template = _pickle.load(file)
    return template

# 生成匹配模板
def get_contours(img, max_threshold, min_threshold, file_path, max_num_points=128):
    '''
    img: 输入图片
    max_threshold: 高阈值（大于该值视为强边缘）
    min_threshold: 低阈值（小于该值直接删掉）
    file_path: 模板文件保存地址
    max_num_points: 模板中点的最大数量
    '''
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img[:, :, 0]
    else:
        gray = img
    # 双边滤波 保边降噪
    temp = cv2.bilateralFilter(gray,9,75,75)
    # 计算梯度与角度
    sobel_dx, sobel_dy, magnitude, sobel_ag = _gen_magnitude(temp, angle=True)
    # 非极大值抑制
    nms_edges = _nms(magnitude, sobel_ag)
    # 滞后阈值
    img_edge = _double_threshold(nms_edges, max_threshold, min_threshold)
    # 生成模板文件
    template = _get_template(sobel_dx, sobel_dy, magnitude, img_edge, max_num_points)
    # 保存模板文件
    _save_template(template, file_path)

    # 显示找到的轮廓点
    img_show = np.stack([gray,gray,gray],axis=-1)
    points = template['points']
    center = template['center_gravity']
    for i in points:
        cv2.circle(img_show, (int(i[1]+center[1]), int(i[0]+center[0])), 2, (0, 0, 255), -1)
    cv2.imshow('', img_show)
    cv2.waitKey(0)





# *************************************************************
# 第二步，使用滑动窗口的边缘模板匹配
def matching(img, file_temp, min_score, greediness):
    '''
    img: 输入图片
    file_temp: 模板文件路径
    min_score: 最小阈值0-1（当匹配分数小于该阈值时停止该次匹配）
    greediness: 贪婪程度0-0.999999（匹配模板的百分比：只有匹配完一定程度的模板后才会放弃本次匹配，避免首先匹配对象的缺失部分时漏检）
    '''
    # 载入模板
    template = _read_template(file_temp)
    number_point = template['points_number']
    points_temp = template['points']
    grad_temp_y = template['gradient_y']
    grad_temp_x = template['gradient_x']
    magnit_temp = template['magnitude']

    # 图像预处理
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img[:, :, 0]
    else:
        gray = img
    h, w = gray.shape
    temp = cv2.bilateralFilter(gray,9,75,75)
    sobel_dx, sobel_dy, magnitude, sobel_ag = _gen_magnitude(temp)

    # 采用滑动窗口匹配,假设每个像素都可能为模板图像的重心 NCC
    result_points = []
    for i in range(h):
        for j in range(w):
            partial_sum = 0
            for m in range(number_point):
                # 计算对应点坐标
                y_matchimg = i + points_temp[m][0]
                x_matchimg = j + points_temp[m][1]
                grad_t_y = grad_temp_y[m]
                grad_t_x = grad_temp_x[m]

                if y_matchimg<0 or x_matchimg<0 or y_matchimg>h-1 or x_matchimg>w-1:
                    continue

                grad_m_y = sobel_dy[y_matchimg, x_matchimg]
                grad_m_x = sobel_dx[y_matchimg, x_matchimg]

                if grad_m_y !=0 or grad_m_x != 0:
                    partial_sum += (grad_m_y*grad_t_y + grad_m_x*grad_t_x) * magnit_temp[m] / magnitude[y_matchimg,x_matchimg]
                # partial_score反应图像和模板匹配程度(最大为1)，越大匹配程度越高
                partial_score = partial_sum / (m + 1)

                # 设置阈值 当匹配一定程度后，总拟合程度仍小于阈值时，取消该次匹配
                norm_minscore = min_score / number_point  # 预计算min_score
                norm_greediness = ((1-greediness*min_score)/(1-greediness)) / number_point  # 预计算greediness
                if partial_score < min((min_score -1 + norm_greediness*(m+1)), norm_minscore*(m+1)):
                    break

            if partial_score > min_score:
                result_points.append([i,j])
        print('\r', (i+1), '/', h, end='')   # 匹配进度

    # 显示匹配到的对象
    img_show = np.stack([gray,gray,gray],axis=-1)
    for y, x in result_points:
        for i, j in points_temp:
            cv2.circle(img_show, (int(j+x), int(i+y)), 1, (0, 0, 255), -1)
    cv2.imshow('', img_show)
    cv2.waitKey(0)

    return result_points



if __name__ == '__main__':
    '''
    目前该算法没有旋转 缩放 匹配功能  但对于背景颜色变化或工件部分被遮挡依旧有效
    优化方向：使用金字塔方法 加入旋转不变性
    '''
    # 生成模板
    template = cv2.imread(r'./image/template_contours.jpg',0)
    file_temp = r'./image/template_contours.info'
    # get_contours(template, 50, 20, file_temp,300)

    # 匹配
    img = cv2.imread(r'./image/template_001.jpg')
    matching(img, file_temp, 0.8, 0.2)


    # cv2.imshow('', img_show)
    # cv2.waitKey(0)



# https://blog.csdn.net/jpc20144055069/article/details/106392282