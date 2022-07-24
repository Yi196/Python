import cv2, os
import numpy as np
import math

#计算梯度与梯度方向
def _gen_magnitude(img):
    sobel_dx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    sobel_dy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
    magnitude = np.sqrt(sobel_dx * sobel_dx + sobel_dy * sobel_dy)
    sobel_ag = cv2.phase(sobel_dx, sobel_dy, angleInDegrees=True)
    return magnitude, sobel_ag

def line_segment_detection(img, scale=0.8, sigma=1, quant=2.0, ang_th=45,
                           log_eps=0.0, density_th=0.7, n_bins=1024):
    '''
    输入：
    img: 图像
    scale: 图像降采样率
    quant: 梯度量化误差
    ang_th: 允许的梯度角度公差
    log_eps: 检测阈值：-log10(NFA) > log_eps
    density_th: 矩形内的采样密度
    n_bins: 梯度模伪排序数量
    输出：
    n_out: lsd算法检测得到的线段的数量n，return的返回值是n条线段，为一维double型数组，长度为8*n，每8个为一组，存着x1,y1,x2,y2,dx,dy,width,polarity
    reg_img: 输出标记区域，是一维的int型数组，大小reg_y*reg_x,在相应的像素位置标记着它属于的线段(1,2,3,...n),如果值为0表示不属于任何线段.
    '''
    # 角度公差
    prec = math.pi * ang_th / 180.0
    p = ang_th / 180.0
    rho = quant / math.sin(prec)  # 梯度幅度阈值
    # if scale != 1.0:
    #     img = cv2.resize(img, None, fx=scale, fy=scale)
    img = cv2.GaussianBlur(img, (3, 3), sigmaX=sigma, borderType=cv2.BORDER_REPLICATE)
    magnitude, sobel_ag = _gen_magnitude(img)


    cv2.imshow('11',magnitude)
    cv2.imshow('22',sobel_ag)
    cv2.waitKey(0)

def detect_circle(img):
    hight, width = img.shape[:2]
    data = img.reshape(-1).astype(np.float64)  # 按行展开为一行
    line_segment_detection(img)




    # cv2.imshow('11',img)
    # cv2.waitKey(0)

if __name__ == '__main__':
    path = r'C:\Users\dihuge\Desktop\Circle-detection-master\code\6.jpg'
    img = cv2.imread(path,0)
    detect_circle(img)