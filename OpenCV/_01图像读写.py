import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# 读取
img = cv.imread(r'image/001.jpg', 1)   # 默认1 忽略透明度   0 灰度图  -1 带透明度
img2 = cv.imread(r'image/001.jpg', 0)
img2 = cv2.imdecode(np.fromfile(r'image/001.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)    # 路径含有中文


'''#以opencv显示  弹出窗口 不推荐
cv.imshow('窗口1',img)
cv.waitKey()  #等待图像绘制  若为cv.waitKey(0) 则永远等待直至图像显示出来
cv.destroyAllWindows()  #关闭窗口'''

# 以matplotlib显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.imshow(img[:, :, ::-1])    # 彩色图片要将opencv的BGR格式 转为RGB才能显示
plt.title('Result'), plt.xticks([]), plt.yticks([])
plt.show()
plt.imshow(img2,cmap=plt.cm.gray)   # 灰度图片指定 cmap=plt.cm.gray
plt.title('Result'), plt.xticks([]), plt.yticks([])
plt.show()

# 保存图片
cv.imwrite(r'image/002.jpg', img2)
cv2.imencode('.jpg', img2)[1].tofile(r'image/002.jpg')   # 路径含有中文


# 添加高斯噪声
def img_nois(img, sigma=20, ratio=1.0):
    return np.clip(np.round((img + np.random.randn(*img.shape)*sigma)*ratio), 0, 255).astype(np.uint8)

cv2.imshow('img_nois', img_nois(img))
cv2.waitKey(0)

# 图像增强评价函数
def psnr(img_reference, img_denoise):
    return 10*np.log10(255*255.0/(((np.double(img_reference)-img_denoise)**2).mean()))

# 计算图像清晰度

# 将图像转换为灰度图像
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 计算图像的Laplacian变换
laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)

# 计算图像的清晰度得分
sharpness = laplacian.var()
print("图像清晰度得分：", sharpness)

# 减小计算量
scale = cv2.Sobel(img[0], cv2.CV_8U, 1, 0)
sharpness = scale.var()
print(sharpness)