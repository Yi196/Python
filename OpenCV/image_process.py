import cv2
import numpy as np
import pdb
import time

def skelenton(binary):
    # 生成一个二值化图像的骨架
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    size = np.size(binary)
    skel = np.zeros_like(binary)

    while True:
        eroded = cv2.erode(binary, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(binary, temp)
        skel = cv2.bitwise_or(skel, temp)
        binary = eroded.copy()
        zeros = size - cv2.countNonZero(binary)
        if zeros == size:
            break
    return skel

def trans_xy_rotate(img, delta_w, delta_h, angle):
    '''
    生成新图像，先平移，后旋转
    :param img:
    :param delta_w:
    :param delta_h:
    :param angle:
    :return:
    '''
    img = trans_xy(img, delta_w, delta_h)
    rotate_ret = rotate(img, angle)
    return rotate_ret['image']

def trans_xy(img, delta_w, delta_h, pad=None):
    # 生成一个新的图像，按照delta的值偏移，delta是指原来是0，新的点是delta
    h, w = img.shape[:2]
    if delta_h is not None and abs(delta_h) > h:
        return None
    if delta_w is not None and abs(delta_w) > w:
        return None
    base = np.zeros_like(img)
    if pad is not None:
        base = base + pad
    base_start_w = 0
    base_end_w = w
    base_start_h = 0
    base_end_h = h
    img_start_w = 0
    img_end_w = w
    img_start_h = 0
    img_end_h = h
    if delta_h is not None:
        if delta_h > 0:
            base_start_h = delta_h
            img_end_h = h - delta_h
        elif delta_h < 0:
            base_end_h = h + delta_h
            img_start_h = -delta_h
    if delta_w is not None:
        if delta_w > 0:
            base_start_w = delta_w
            img_end_w = w - delta_w
        elif delta_w < 0:
            base_end_w = w + delta_w
            img_start_w = -delta_w
    base[base_start_h:base_end_h, base_start_w:base_end_w] = img[img_start_h:img_end_h, img_start_w:img_end_w]
    return base


def rotate(image, angle, center=None, scale=1.0, line_dict=None, pt=None, pts=None):
    # 旋转
    # line_dict: key是朝向，val是list 每个元素是x0,y0,x1,y1
    # 获取图像尺寸
    ret_dict = {
        'valid': False,
        'image': None,
        'lines': None,
        'M': None,
        'pt': None,
        'pts': None,
    }
    (h, w) = image.shape[:2]

    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)

    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    ret_dict['M'] = M
    rotated = cv2.warpAffine(image, M, (w, h))
    ret_dict['image'] = rotated
    if line_dict is not None:
        new_line_dict = {}
        pts = []
        for orient, lines in line_dict.items():
            one_pts = []
            num_line = len(lines)
            if num_line == 0:
                continue
            for line in lines:
                one_pts.append(line[:2])
                one_pts.append(line[2:])
            one_pts = np.expand_dims(one_pts, axis=1)
            pts.append(one_pts)
            new_pts = cv2.transform(one_pts, M)
            # new_lines = []
            # for i in range(num_line):
            #     new_lines.append((new_pts[i*2,0,0], new_pts[i*2,0,1], new_pts[i*2+1,0,0], new_pts[i*2+1,0,1]))
            new_line_dict[orient] = new_pts
        ret_dict['lines'] = new_line_dict
    if pt is not None:
        new_pt = cv2.transform(pt, M)
        ret_dict['pt'] = new_pt.astype(np.int32)
    if pts is not None:
        new_pts = cv2.transform(pts, M)
        ret_dict['pts'] = new_pts.astype(np.int32)
    ret_dict['valid'] = True
    return ret_dict

def biggest_component(img, topk=1):
    # 只保留最大topk个连通域，干掉其他的，如果没有白色区域，返回None
    ret_dict = {
            'binary': img,
            'status': [],
            }
    t0 = time.time()
    labels, ccm, status, centers = cv2.connectedComponentsWithStats(img)
    t1 = time.time()
    max_area = 0
    max_idx = -1
    sort_label = np.argsort(status[:, 4], axis=-1)[::-1]
    if sort_label.shape[0] == 0:
        return ret_dict
    black_lab = None
    h, w = img.shape
    # 四个角大概率是黑的
    corners = [[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]]
    for corner in corners:
        if img[corner[1], corner[0]] == 0:
            black_lab = ccm[corner[1], corner[0]]
            break
    used_labs = []
    for i in range(labels):
        if len(used_labs) == topk:
            break
        lab = sort_label[i]
        if black_lab is not None:
            if lab == black_lab:
                continue
            else:
                used_labs.append(lab)
        else:
            idx = np.where(ccm == lab)
            color = img[idx[0][0], idx[1][0]]
            if color == 0:
                black_lab = lab
            else:
                used_labs.append(lab)
    base = np.zeros((h, w), np.uint8)
    for lab in used_labs:
        idx = np.where(ccm == lab)
        base[idx] = 255
        ret_dict['status'].append(status[lab])
    ret_dict['binary'] = base
#    cv2.imshow('base', base)
#    cv2.waitKey(0)
    return ret_dict

def biggest_two_component(img):
    # 只保留最大两个连通域，干掉其他的，白色区域不够，返回None
    ret_dict = {
        'big': None,
        'small': None,
    }
    labels, ccm, status, _ = cv2.connectedComponentsWithStats(img)
    areas = []
    have_labels = []
    for i in range(labels):
        idx = np.where(ccm == i)
        if idx[0].shape[0] == 0:
            return None
        if ccm[idx[0][0], idx[1][0]] == 0:
            continue
        area = len(idx[0])
        areas.append(area)
        have_labels.append(i)
    if len(areas) < 2:
        return ret_dict
    area_idx = np.argsort(areas)
    # pdb.set_trace()
    for i in range(2):
        base = np.zeros_like(img)
        num = -1 - i
        idx = np.where(ccm == have_labels[area_idx[num]])
        base[idx] = 255
        # cv2.imshow('base', base)
        # cv2.waitKey(0)
        if i == 0:
            ret_dict['big'] = base
        else:
            ret_dict['small'] = base
    return ret_dict

def gen_magnitude(img):
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

def safe_crop(image, cent, left, right, top, bottom):
    '''
    该函数用于输入一个定位点cent坐标，从定位点向上下左右截取固定像素值的图片
    image:
    cent: (x, y)
    left: offset 向左
    '''
    h, w = image.shape[:2]
    x0 = max(0, int(cent[0]-left+0.5))
    y0 = max(0, int(cent[1]-top+0.5))
    x1 = min(w-1, int(cent[0] + right + 0.5))
    y1 = min(h-1, int(cent[1] + bottom + 0.5))
    if y1 - y0 >= 0 or x1-x0 >=0:
        roi = image[y0:y1, x0:x1]
    else:
        roi = None
    pts = [x0, y0, x1, y1]
    ret_dict = {
            'image': roi,
            'pts': pts,
            }
    return ret_dict

