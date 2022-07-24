import cv2
import numpy as np

#连通区域一般是指图像中具有相同像素值且位置相邻的前景像素点组成的图像区域。连通区域分析是指将图像中的各个连通区域找出并标记
img = cv2.imread(r'./image/003.jpg', 0)
ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

#connectedComponents()仅仅创建了一个标记图（图中不同连通域使用不同的标记，和原图宽高一致
num_objects, labels_1 = cv2.connectedComponents(binary)   #输入为单通道二值化图像
#返回值：所有连通域的数目 labels_1：图像上每一像素的标记，用数字1、2、3…表示（不同的数字表示不同的连通域）


#connectedComponentsWithStats()可以完成上面任务，除此之外，还可以返回每个连通区域的重要信息–bounding box, area, andcentroid。
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8, ltype=None) #connectivity：可选值为4或8，也就是使用4连通还是8连通。
#stats：每一个标记的统计信息，是一个5列的矩阵，每一行对应每个连通区域的外接矩形的x、y、width、height和面积，示例如下： 0 0 720 720 291805
#centroids：连通域的中心点

print(num_labels) #所有黑色也是一个连通区域
# print(labels)  #labels==0表示黑色区域
print(stats.shape)


# 不同的连通域赋予不同的颜色
output = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
for i in range(1, num_labels):

    mask = labels == i

    output[:, :, 0][mask] = np.random.randint(0, 255)
    output[:, :, 1][mask] = np.random.randint(0, 255)
    output[:, :, 2][mask] = np.random.randint(0, 255)
cv2.imshow('oginal', output)
cv2.waitKey()
cv2.destroyAllWindows()


#找最大连通区域
def biggest_component(binary):
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8, ltype=None)
    #找最大连通区域所在索引
    temp = stats[:,4].argsort()
    idx = temp[-1] if temp[-1] else temp[-2]   # 最大爲背景時捨去
    # width, height = stats[idx][2:4]
    # print(stats, '\n', width, height)
    temp_l = np.zeros_like(labels)
    temp_l[labels == idx] = 255
    temp_l = temp_l.astype(np.uint8)

    return temp_l


if __name__ == '__main__':
    img = cv2.imread(r'./image/003.jpg', 0)
    ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    ret_img = biggest_component(binary)
    cv2.imshow('', ret_img)
    cv2.waitKey()