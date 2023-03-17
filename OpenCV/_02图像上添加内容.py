import numpy as np
import cv2
import matplotlib.pyplot as plt

img = np.zeros((500,500,3), dtype=np.uint8)  # 生成黑色图片 注意为8位无符号整型
print(img.shape)
print(img.dtype)
print(img.size)
# 直线
cv2.line(img, (0,0), (500,500), color=(255,0,0), thickness=5)   # 注意为RGB颜色 在opencv中为BGR   #thickness 为线宽

# 圆
cv2.circle(img, (250,250), radius=100, color=(45,100,200))
cv2.circle(img, (100,100), radius=40, color=(0,255,0), thickness=-1)  # 圆中 thickness=—1 表示将整个圆涂满颜色

# 椭圆
cv2.ellipse(img, (250,250), (100,200), 90, 0, 360, (145,80,140), thickness=1)  # 图 椭圆中心 长短轴 旋转角 起始角度 结束角度 颜色 线宽

# 矩形
cv2.rectangle(img, (0,400), (300,500), color=(76,28,179), thickness=10)  # 矩形 给出左上 右下坐标

# Opencv显示中文
from PIL import Image, ImageDraw, ImageFont
def cv2ImgAddText(img, text, bottom_left, color=(0, 255, 0), textSize=20):
    if isinstance(img, np.ndarray):   # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(r"./image/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    left_top = (bottom_left[0], bottom_left[1] - textSize)
    draw.text(left_top, text, color, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

# 文字
font=cv2.FONT_HERSHEY_COMPLEX # 字体
cv2.putText(img, 'Opencv', (250,250), font, 1, color=(255,255,255), thickness=2, lineType=cv2.LINE_AA)  # cv2.LINE_AA表示以线形写入 可省 位置为左下角坐标
img = cv2ImgAddText(img, '中文测试', (300, 300), (255, 255, 255), 20)  # 写中文

# 带箭头直线
cv2.arrowedLine(img, (10,10), (200,300), (0,128,255), thickness=2, line_type=8, shift=2, tipLength=0.2)
# line_type(int): 绘制线的类型，-1就是FILLED（填满），4是LINE_4（4连通域），8是LINE_8（8连通域），LINE_AA（抗锯齿线）
# shift(int): 数值可以控制箭头的长度和位置，比如当其为1时，箭头的位置变为原先的1/2，长度也变为1/2，若该数值为2，则均变为原先的1/4
# tipLength(double): 箭头和箭身的比例，默认为0.1

# 根据多个点的坐标填充多边形
img_3 = np.zeros((1080, 1920, 3), np.uint8)
triangle = np.array([[0, 0], [1500, 800], [500, 400]])  # 逆时针 多边形顶点坐标
cv2.fillConvexPoly(img_3, triangle, (255, 255, 255))


# 填充多个多边形
img_4 = np.zeros((1080,1920,3), np.uint8)
area1 = np.array([[250, 200], [300, 100], [750, 800], [100, 1000]])
area2 = np.array([[1000, 200], [1500, 200], [1500, 400], [1000, 400]])
cv2.fillPoly(img_4, [area1, area2], (255, 255, 255))


# 绘制多边形(可多个，根据多边形顶点坐标绘制边)
img_5 = np.zeros((1080,1920,3), np.int8)
pts = np.array([[[250, 200], [300, 100], [750, 800], [100, 1000]],       # 两个四边形shape为[2,4,2]
                [[1000, 200], [1500, 200], [1500, 400], [1000, 400]]])
pts2 = [np.array([[250, 200], [300, 100], [750, 800], [100, 1000]]),
        np.array([[1000, 200], [1500, 200], [1500, 400], [1000, 400], [800, 150]])]   # 当多边形的边数不一致时，不能直接使用np.array() np.asarray(), 这两个函数都要求数组内部维度一致
img_5 = cv2.polylines(img_5, pts2, isClosed=True, color=(255, 125, 125), thickness=4, lineType=cv2.LINE_AA)  # isClosed=True 所画多边形闭合


# 绘制带角度的矩形
img_1 = cv2.imread(r'./image/003.jpg')
gray = cv2.cvtColor(img_1,cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
# _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # opencv3.4
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
rect = cv2.minAreaRect(contours[0])
box = cv2.boxPoints(rect)                                  # 先提取点集
cv2.drawContours(img_1, [np.int0(box)], 0, (0,0,255),2)    # 再绘制图像
cv2.polylines(img_1, [np.int0(box)], True, (255,0,0),2)    # 也可用此函数绘制图像


# 给图像绘制边框
# cv2.copyMakeBorder(src, top, bottom, left, right, borderType,value)
'''
src ：输入的图片
top, bottom, left, right ：相应方向上的边框宽度
borderType：定义要添加边框的类型，它可以是以下的一种：
cv2.BORDER_CONSTANT：添加的边界框像素值为常数（需要额外再给定一个参数）
cv2.BORDER_REFLECT：添加的边框像素将是边界元素的镜面反射，类似于gfedcb|abcdefgh|gfedcba
cv2.BORDER_REFLECT_101 or cv2.BORDER_DEFAULT：和上面类似，但是有一些细微的不同，类似于gfedcb|abcdefgh|gfedcba
cv2.BORDER_REPLICATE：使用最边界的像素值代替，类似于aaaaaa|abcdefgh|hhhhhhh
cv2.BORDER_WRAP：不知道怎么解释，直接看吧，cdefgh|abcdefgh|abcdefg
value：如果borderType为cv2.BORDER_CONSTANT时需要填充的常数值。
'''
img_005 = cv2.imread('./image/005.jpg')
ret_1 = cv2.copyMakeBorder(img_005, 50, 50, 50, 50, cv2.BORDER_REFLECT)
ret_2 = cv2.copyMakeBorder(img_005, 50, 50, 50, 50, cv2.BORDER_REPLICATE)
ret_3 = cv2.copyMakeBorder(img_005, 50, 50, 50, 50, cv2.BORDER_WRAP)



# 显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.imshow(img[:, :, ::-1])
plt.title('Result'), plt.xticks([]), plt.yticks([])
plt.show()
plt.imshow(img_3[:, :, ::-1])
plt.title('Result'), plt.xticks([]), plt.yticks([])
plt.show()
plt.imshow(img_4[:, :, ::-1])
plt.title('Result'), plt.xticks([]), plt.yticks([])
plt.show()
plt.imshow(img_5[:, :, ::-1])
plt.title('Result'), plt.xticks([]), plt.yticks([])
plt.show()
plt.imshow(img_1, plt.cm.gray)
plt.title('Result'), plt.xticks([]), plt.yticks([])

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8, 3), dpi=100)
axes[0].imshow(ret_1[:, :, ::-1])
axes[0].set_title('边界元素的镜面反射')
axes[1].imshow(ret_2[:, :, ::-1])
axes[1].set_title('最边界的像素值代替')
axes[2].imshow(ret_3[:, :, ::-1])
axes[2].set_title('..')
plt.show()