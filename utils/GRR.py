import cv2,os
import numpy as np


def _detect_roi(image, orient, brightness, max_pts_num, min_pts_num, mag_thresh, is_subpixel=True, n=5):
    '''
    one image, one roi
    返回值：
    line_point: [x0,y0,x1,y1]  拟合的直线起始点坐标
    coeff: [0,k,b] 拟合直线的系数 0表示成功拟合直线-1：线未拟合成功
    pts:[[x1,y1],[x2,y2],..] 拟合直线所用到的点
    '''

    h, w = image.shape
    mag, mag_angle = _gen_magnitude(image)
    delete_ranges = []
    # 删除梯度方向不对的点
    if orient == '从右到左':
        if brightness == '从白到黑':
            delete_ranges.append((120, 240))
        elif brightness == '从黑到白':
            delete_ranges.append((0, 60))
            delete_ranges.append((300, 360))
    elif orient == '从上到下':
        if brightness == '从白到黑':
            delete_ranges.append((30, 150))
        elif brightness == '从黑到白':
            delete_ranges.append((210, 330))
    elif orient == '从下到上':
        if brightness == '从白到黑':
            delete_ranges.append((210, 330))
        elif brightness == '从黑到白':
            delete_ranges.append((30, 150))
    elif orient == '从左到右':
        if brightness == '从白到黑':
            delete_ranges.append((0, 60))
            delete_ranges.append((300, 360))
        elif brightness == '从黑到白':
            delete_ranges.append((120, 240))
    for bound in delete_ranges:
        mag[np.logical_and(mag_angle >= bound[0], mag_angle <= bound[1])] = 0
    # '从右到左', '从左到右'
    if orient in ['从右到左', '从左到右']:
        if orient == '从右到左':
            max_h = mag.shape[1] - np.argmax(mag[:, ::-1], axis=1) - 1
        else:
            max_h = np.argmax(mag, axis=1)

        pts = np.stack([max_h, np.array(range(mag.shape[0]), np.int32)], axis=0)  #pts=[[x1,x2..],[y1,y2..]]
        num = max_h.shape[0]
        if num > max_pts_num:
            used = np.linspace(0, num, max_pts_num, endpoint=False)
            used = used.astype(np.int32)
            used_num = used.shape[0]
        else:
            used = pts[1, :]
            used_num = num

        if is_subpixel:
            sub_pts = []
            # subpixel
            for i in range(used_num):
                cur_y = pts[1, used[i]]
                cur_x = pts[0, used[i]]
                if mag[cur_y, cur_x] < mag_thresh:
                    continue
                if cur_x == 0 or cur_x == w - 1:
                    sub_pts.append((cur_x, cur_y))
                else:
                    val = mag[cur_y, cur_x - 1] + mag[cur_y, cur_x + 1] - 2 * mag[cur_y, cur_x]
                    sign = np.sign(val)
                    if sign == 0:
                        sign = 1
                    sub_offset = (mag[cur_y, cur_x - 1] - mag[cur_y, cur_x + 1]) / (sign * max(0.0001, abs(val))) / 2
                    sub_pts.append((sub_offset + cur_x, cur_y))
            # 竖直方向角度需考虑数值精度问题
            pts = np.array(sub_pts)     #pts=[[x1,y1],[x2,y2]..]
        else:
            pts = (pts[:, used]).transpose()

        if pts.shape[0] - n < min_pts_num or pts.shape[1] != 2:
            coeff = np.array([-1, -1, -1])
            return None, coeff, None
        else:
            #先拟合一次直线
            coeff = np.polyfit(pts[:,1], pts[:,0], 1)   #此处拟合x=k1y+b1,反算出y=kx+b中的k，b
            sign = np.sign(coeff[0])
            if sign == 0:
                sign = 1
            k = 1 / (sign * max(np.abs(coeff[0]), 0.0001))
            coeff = np.array((0, k, - coeff[1] * k))
            line_point = _coeff2pts(image, coeff[1:])
            #删除n个异常点
            pts = _del_max_distance_point(pts, line_point, n)
            #再拟合一次
            coeff = np.polyfit(pts[:, 1], pts[:, 0], 1)
            sign = np.sign(coeff[0])
            if sign == 0:
                sign = 1
            k = 1 / (sign * max(np.abs(coeff[0]), 0.0001))
            coeff = np.array((0, k, - coeff[1] * k))
            line_point = _coeff2pts(image, coeff[1:])
            return line_point, coeff, pts

    elif orient in ['从上到下', '从下到上']:
        if orient == '从下到上':
            max_w = mag.shape[0] - np.argmax(mag[::-1, :], axis=0) - 1
        else:
            max_w = np.argmax(mag, axis=0)

        pts = np.stack([np.array(range(mag.shape[1]), np.int32), max_w], axis=0)
        num = max_w.shape[0]
        if num > max_pts_num:
            used = np.linspace(0, num, max_pts_num, endpoint=False)
            used = used.astype(np.int32)
            used_num = used.shape[0]
        else:
            used = pts[0, :]
            used_num = num

        if is_subpixel:
            sub_pts = []
            # subpixel
            for i in range(used_num):
                cur_y = pts[1, used[i]]
                cur_x = pts[0, used[i]]
                if mag[cur_y, cur_x] < mag_thresh:
                    continue
                if cur_y == 0 or cur_y == h - 1:
                    sub_pts.append((cur_x, cur_y))
                else:
                    val = mag[cur_y - 1, cur_x] + mag[cur_y + 1, cur_x] - 2 * mag[cur_y, cur_x]
                    sign = np.sign(val)
                    if sign == 0:
                        sign = 1
                    sub_offset = (mag[cur_y - 1, cur_x] - mag[cur_y + 1, cur_x]) / (sign * max(0.0001, abs(val))) / 2
                    sub_pts.append((cur_x, sub_offset + cur_y))
            pts = np.array(sub_pts)
        else:
            pts = (pts[:, used]).transpose()

        if pts.shape[0] - n < min_pts_num or pts.shape[1] != 2:
            coeff = np.array([-1, -1, -1])
            return None, coeff, None
        else:
            coeff = np.polyfit(pts[:,0], pts[:,1], 1)
            coeff = np.array((0, coeff[0], coeff[1]))
            line_point = _coeff2pts(image, coeff[1:])

            pts = _del_max_distance_point(pts,line_point,n)

            coeff = np.polyfit(pts[:,0], pts[:,1], 1)
            coeff = np.array((0, coeff[0], coeff[1]))
            line_point = _coeff2pts(image, coeff[1:])
            return line_point, coeff, pts


# 去除n个距离最大的点
def _del_max_distance_point(pts,line_point,n=5):
    if n>0:
        line_point1 = np.array([line_point[0], line_point[1]])
        line_point2 = np.array([line_point[2], line_point[3]])
        lst_point = []
        for idx, point in enumerate(pts):
            lst_point.append([idx, _point_distance_line(point, line_point1, line_point2)])
        lst_point.sort(key=lambda x: x[1])
        lst_point = np.array(lst_point[-n:])
        pts = np.delete(pts, (lst_point[:,0]).astype(np.int64), axis=0)  #注意索引要为整数 np.int64
        return pts

# 计算点到直线距离
def _point_distance_line(point,line_point1,line_point2):
    # 计算向量
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(line_point1 - line_point2)
    return distance


# 计算梯度与梯度方向
def _gen_magnitude(img):
    '''
    计算图像的梯度特征
    :param img:
    :return:
    '''
    smoothed = cv2.GaussianBlur(img, (3, 3), 0, sigmaY=0, borderType=cv2.BORDER_REPLICATE)
    sobel_dx = cv2.Sobel(smoothed, cv2.CV_32F, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    sobel_dy = cv2.Sobel(smoothed, cv2.CV_32F, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    magnitude = np.sqrt(sobel_dx * sobel_dx + sobel_dy * sobel_dy)
    sobel_ag = cv2.phase(sobel_dx, sobel_dy, angleInDegrees=True)
    return magnitude, sobel_ag

# 计算拟合直线端点坐标
def _coeff2pts(image, coeff):
    '''
    计算拟合直线的起始点坐标
    coeff: coeff[0] * x + coeff[1] = y
    返回值
    pts: [x0,y0,x1,y1]
    '''
    h, w = image.shape[:2]
    pts = []
    sign = np.sign(coeff[0])
    if sign == 0:
        sign = 1
    inv_k = sign * 1 / max(np.abs(coeff[0]), 0.0001)
    x0 = 0
    y0 = coeff[1]
    if y0 >= 0 and y0 <= h - 1:
        pts.append((x0, y0))
    y0 = 0
    x0 = - coeff[1] * inv_k
    if x0 >= 0 and x0 <= w - 1:
        pts.append((x0, y0))
    if len(pts) == 2:
        pts = [pts[0][0], pts[0][1], pts[1][0], pts[1][1]]
        return pts
    x0 = w - 1
    y0 = coeff[0] * x0 + coeff[1]
    if y0 >= 0 and y0 <= h - 1:
        pts.append((x0, y0))
    if len(pts) == 2:
        pts = [pts[0][0], pts[0][1], pts[1][0], pts[1][1]]
        return pts
    y0 = h - 1
    x0 = (y0 - coeff[1]) * inv_k
    if x0 >= 0 and x0 <= w - 1:
        pts.append((x0, y0))
    pts = [pts[0][0], pts[0][1], pts[1][0], pts[1][1]]
    return pts



def detect_line_subpixel(img,
                         rect,
                         orient='从左到右',
                         brightness='从白到黑',
                         max_pts_num=80,
                         min_pts_num=5,
                         mag_thresh=50,
                         is_subpixel=True,
                         n=5):
    '''
    images: 输入图像
    rect: list [x0, y0, x1, y1]  找线区域 输入任意两对角坐标
    orient: str  '从左到右','从右到左','从上到下','从下到上' （方向）
    brightness: str '从白到黑','从黑到白'
    max_pts_num: int, 最大点数
    min_pts_num: int, 最小点数
    mag_thresh: int, magnitude/gray thresh 梯度阈值/灰度阈值
    is_subpixel: 亚像素精度
    n: int 剔除距离最大的n个点

    返回值：
    line_point: [x0,y0,x1,y1]  拟合的直线起始点坐标
    coeff: [k,b] 拟合直线的系数
    pts:[[x1,y1],[x2,y2],..] 拟合直线所用到的点
    angle: float  拟合直线的角度
    '''

    assert img is not None, "img is not None!"

    #转为单通道灰度图
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img[:, :, 0]
    else:
        gray = img

    x0, y0, x1, y1 = np.rint(rect).astype(np.int32)
    if x1 < x0 and y1 < y0:
        x0,x1 = x1,x0
        y0,y1 = y1,y0
    elif x0 < x1 and y0 > y1:
        y0, y1 = y1, y0
    elif x0 > x1 and y0 <y1:
        x0, x1 = x1, x0

    roi = gray[y0:y1, x0:x1]


    line_point, coeff, pts = _detect_roi(roi, orient, brightness, max_pts_num, min_pts_num, mag_thresh, is_subpixel, n)

    if coeff[0] == 0:
        line_point[0] = line_point[0] + x0
        line_point[1] = line_point[1] + y0
        line_point[2] = line_point[2] + x0
        line_point[3] = line_point[3] + y0
        pts[:, 0] = pts[:, 0] + x0
        pts[:, 1] = pts[:, 1] + y0
        coeff = coeff[1:]
        # 计算直线倾斜角度
        angle = np.arctan(coeff[0]) * 57.29577

        # 显示用来拟合直线的点和直线
        img = np.stack([gray,gray,gray],axis=-1).astype(np.uint8)
        for x,y in pts:
            cv2.circle(img,(int(x),int(y)),2,(0,0,255),-1)
        x0, y0, x1, y1 = line_point
        # cv2.line(img,(int(x0),int(y0)),(int(x1),int(y1)),(0,0,255),2)
        cv2.namedWindow('001',0)
        cv2.resizeWindow('001',1920,1080)
        cv2.imshow('001',img)
        cv2.waitKey(0)

        return line_point, coeff, pts, angle
    else:
        return None, None, None, None


def _calculate_size(lst_point):
    x0, y0, x1, y1 = lst_point[0]
    x_mid, y_mid = (x0+x1)/2, (y0+y1)/2
    lx0, ly0, lx1, ly1 = lst_point[1]

    distance_lst = []
    for i in [np.array([x0,y0]), np.array([x_mid,y_mid]), np.array([x1,y1])]:
        distance_lst.append(_point_distance_line(i, np.array([lx0,ly0]), np.array([lx1,ly1])))
    distance = np.mean(distance_lst)
    # print(distance)
    return distance


def detect_size(img, rects, orient, brightness, max_pts_num, min_pts_num, mag_thresh, n, pixel=0.004296):
    count = 0
    lst_point = []
    distance_lst = []
    angle_lst = []
    angle_average = []
    for r, o in zip(rects, orient):
        line_point, _, _, angle = detect_line_subpixel(img, r, o, brightness, max_pts_num, min_pts_num,mag_thresh, n=n)
        lst_point.append(line_point)
        angle_lst.append(angle)
        count += 1
        if count % 2 == 0:
            distance_lst.append(_calculate_size(lst_point[-2:]))
            angle_average.append((angle_lst[-1] + angle_lst[-2])/2)
    # print(distance_lst)
    distance_lst = np.array(distance_lst) * pixel
    return distance_lst, angle_average




if __name__ == '__main__':
    global_lst = []
    def get_xy(img):
        def getpos(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # print((x, y), '  ', img[y, x])
                global global_lst
                if global_lst == [] or len(global_lst[-1]) == 4:
                    global_lst.append([x, y])
                else:
                    global_lst[-1].extend([x, y])
                    # global_lst.append(global_lst[-1])

        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('img', 1920, 1080)
        cv2.imshow('img', img)
        cv2.setMouseCallback('img', getpos)
        cv2.waitKey(0)


    # rects = [[2182, 476, 2143, 2085], [2338, 476, 2313, 2197]]
    # orient = ['从左到右', '从右到左']
    orient = ['从上到下', '从下到上']
    brightness = '从白到黑'
    max_pts_num = 600
    min_pts_num = 20
    mag_thresh = 30
    n = 20
    pixel = 0.003125  # 像素精度


    # dir = r'C:\Users\dihuge\Desktop\10_6'
    dir = r'./template'
    dir_wdistance = r"C:\Users\dihuge\Desktop\113.txt"
    with open(dir_wdistance, "a+", encoding="utf-8") as file:
        file.write('\n'+'666'+'\n')

    names = os.listdir(dir)
    for name in names:
        img = cv2.imread(os.path.join(dir,name))
        get_xy(img)
        # print(global_lst)
        rects = global_lst
        global_lst = []
        _, angle_lst = detect_size(img, rects, orient, brightness, max_pts_num, min_pts_num, mag_thresh, n, pixel)
        # print(angle_lst)
        # 旋转
        angle = angle_lst[0]
        # M = cv2.getRotationMatrix2D(center=(img.shape[1]//2, img.shape[0]//2), angle=90+angle if angle<0 else -(90-angle), scale=1)
        M = cv2.getRotationMatrix2D(center=(img.shape[1]//2, img.shape[0]//2), angle=angle if angle<0 else -angle, scale=1)
        img_ro = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
        # 旋转后图像
        # cv2.namedWindow('im', cv2.WINDOW_NORMAL)
        # cv2.imshow('im', img_ro)
        # cv2.waitKey(0)

        temp_lst = []
        for x0,y0,x1,y1 in rects:
            P1 = np.array([x0, y0])
            Q1 = np.dot(M, np.array([[P1[0]], [P1[1]], [1]]))
            x0, y0 = list(Q1[0])[0], list(Q1[1])[0]
            P2 = np.array([x1, y1])
            Q2 = np.dot(M, np.array([[P2[0]], [P2[1]], [1]]))
            x1, y1 = list(Q2[0])[0], list(Q2[1])[0]
            if x0<0 or y0<0 or x1<0 or y1<0:
                raise ValueError("旋转后坐标超出图片范围!!!")
            temp_lst.append([x0,y0,x1,y1])
        # print(temp_lst)
        rects = temp_lst
        distance, _ = detect_size(img_ro, rects, orient, brightness, max_pts_num, min_pts_num, mag_thresh, n, pixel)
        print(distance)
        with open(dir_wdistance, "a+", encoding="utf-8") as file:
            file.write(str(distance[0])+'\n')