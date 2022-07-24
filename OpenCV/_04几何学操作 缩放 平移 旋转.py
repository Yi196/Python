import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('image/001.jpg')

# 绝对值缩放
rows,cols= img.shape[:2]   # 此处为对 (1080, 1920, 3) 切片 得图片尺寸
img1 = cv.resize(img,dsize=(cols*2,rows*2),interpolation=cv.INTER_CUBIC)  # dsize（宽列,高行）为缩放后的绝对尺寸 interpolation插值方法 此处为双三次插值
# 相对值缩放
img2 = cv.resize(img,None,fx=0.5,fy=0.5)

# 移动
M=np.array([                # M为2X3矩阵 指定移动距离
    [1,0,100],              # X移100
    [0,1,50]                # Y移50
], np.float32)              # 注意M为np.float32
img3 = cv.warpAffine(img,M,dsize=(cols,rows))  # dsize为移动后尺寸（列x，行y）

# 旋转
# 先生成旋转矩阵M
M = cv.getRotationMatrix2D(center=(cols//2,rows//2),angle=45,scale=1)   # 旋转中心(列x,行y)此处为图片中心  角度 逆时针  scale 缩放比例
img4 = cv.warpAffine(img,M,(cols,rows))        # (cols,rows)输出图像的尺寸
# 假设某点坐标为P(x,y)，旋转矩阵为M，旋转后图像坐Q可直接有P左乘M得到
P = np.array([0, 0])
Q = np.dot(M, np.array([[P[0]],[P[1]],[1]]))
# 可以使用cv2.invertAffineTransform得到变换矩阵的逆矩阵reverseMatRotation
reverseMatRotation = cv.invertAffineTransform(M)
P = np.dot(reverseMatRotation,np.array([[Q[0]],[Q[1]],[1]]))  # 由旋转后坐标Q(x,y)求对应旋转前坐标P
print(P)

# 仿射变换 （用于深度学习的图像预处理）
pts1 = np.float32([[50,50],[200,50],[50,200]])  # 指定图像上三个点位置
pts2 = np.float32([[100,100],[200,50],[100,250]]) # 指定变换后这三个点的位置
M = cv.getAffineTransform(pts1,pts2)
img5 = cv.warpAffine(img,M,(cols,rows))

# 透视变换
pts1 = np.float32([[56,65],[386,52],[28,387],[389,390]])  # 指定图像上四个点位置
pts2 = np.float32([[100,145],[300,100],[80,290],[310,300]]) # 指定变换后这四个点的位置
T = cv.getPerspectiveTransform(pts1,pts2)
img6 = cv.warpPerspective(img,T,(cols,rows))

# 图像金字塔
img7=cv.pyrUp(img)    # 上采样 扩大
img8=cv.pyrDown(img)  # 下采样
img8=cv.pyrDown(img8)
img8=cv.pyrDown(img8)
img8=cv.pyrDown(img8)


if __name__ == '__main__':
    def show_1(img_1):
        plt.imshow(img_1[:, :, ::-1])
        plt.title('Result'), plt.xticks([]), plt.yticks([])
        plt.show()
    for img_1 in [img1,img2,img3,img4,img5,img6,img7,img8,]:
        show_1(img_1)
