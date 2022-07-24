import cv2
import numpy as np
from PIL import Image
import random


a = np.array([1,2,3,4,5,6,7,8])
# np.histogram(a,bins=5,range=(0,1))计算直方图 bins=（5：均分为五组统计，[1,25,100]:分为[1,25)和[25，100)两组，range=(0,100)表示统计范围）
print(np.histogram(a, bins=3))
print(np.histogram(a, bins=[0, 4, 8], density=True)) # density为True时，返回每个区间的概率密度；为False，返回每个区间中元素的个数

# np.clip()限定数组范围
b = np.clip(a, 3, 6)   # 小于3置为3，大于6置为6 不会改变原数组a

# 按范围搜索
a = np.array([[1,2,3],[4,5,6]])
a[np.where(((a>1)&(a<3)) | ((a>4)&(a<6)))] = 0  # 注意numpy中用 & |
print(a)  #  [[1 0 3]
          #   [4 0 6]]

a = np.array([[1,2,3],[4,5,6]])
# 填充边界（对于二维数组先填充[0]行，再填充列）
np.pad(a, 2, 'symmetric')  # 对称填充(镜像)
np.pad(a, ((2,1),(1,2)), 'constant', constant_values= (1,2))  # 上边填充两行1，下边填充一行2，左边填充一列1，右边填充两列2  先行后列
np.pad(a, ((2,1),(1,2)), 'edge')  # 以边缘填充  先行后列

# np.cumsum(a, axis=None, dtype=None) 累加 axis=0按照行累加 axis=1按照列累加 axis=None将a转为一维数组后累加 dtype=float指定输出数据类型
np.cumsum(a)             # [ 1  3  6 10 15 21]
np.cumsum(a, axis=0)     # [[1 2 3]
                         #  [5 7 9]]

# np.ix_()对多行 列同时赋值
a = np.zeros((6,6))
a[np.ix_([2,3],[0,1])] = 10  # 对第3至4行 1至2列赋值10
# a[2:4, 0:2] = 10

# 高低通滤波
img = cv2.imread(r'./OpenCV/image/007.jpg',0)
# 进行二维傅里叶变换
fft = np.fft.fft2(img)   # 注意numpy的复数只占一个元素，而opencv的复数占两个元素
# 将低频部分移至图像中心（通过掩掉中间位置或四周实现高低通滤波）
fshift = np.fft.fftshift(fft)
# 在fshift上掩膜 略
# 傅里叶逆变换
ifshift = np.fft.ifftshift(fshift)
ifft = np.fft.ifft2(ifshift)


# np.real() np.imag() 返回复数实部、虚部
f_arr = np.array([1+3j, 2+4j])
print(np.real(f_arr))   # 返回实部 [1. 2.]
print(np.imag(f_arr))   # 返回虚部 [3. 4.]


# np.log()计算以e为低的对数,np.log10(),np.square()平方,np.sqrt()平方根,np.exp(x)计算各元素e的x次方,np.power(a,n)计算a中各元素的n次幂,
# np.abs()计算绝对值 复数的模 非复数可用更快的np.fabs(),np.sign()计算正负,np.modf()将数组分为整数和小数两个数组，
# np.nan()判断那些元素为NaN,np.isfinite()/np.isinf()判读那些元素是有穷(非inf非nan)/无穷的,
# np.dot()求两个数组的点积,np.cross()求叉积,

# np.minimum()并返回一个包含按元素的最小值的新数组
min = np.minimum([1,2,3],[3,0,5])  # [1 0 3]

# np.prod()返回指定轴上数组元素的乘积
c1 = np.array([[1,2,3],[4,5,6]])
print(c1.prod(0))  # [ 4 10 18]
print(c1.prod(1))  # [ 6 120]

# 删除索引处元素
a = np.array([[1,2],[3,4],[5,6]])
print(np.delete(a,[0,1],axis=0))   #[[5 6]]

arr_1 = np.array([1,2,3])
arr_2 = np.array([0,1,2])
# np.divide()处理被除数组中含有零
ret = np.divide(arr_1, arr_2, out=np.zeros_like(arr_2, dtype=np.float64), where=arr_2!=0) # 当where为True时，正常除；为False时用out里的对应值替换结果

# 计算点到直线距离
def point_distance_line(point,line_point1,line_point2):
    # 计算向量
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(line_point1 - line_point2)
    return distance

# 求向量叉积 （若a,b均为二维，返回a,b组成平行四边形的面积 有正负）
np.fabs(np.cross([0,2],[1,0]))  # 2

# np.linalg.norm(line_point1 - line_point2) ord=None：表示求整体的矩阵元素平方和，再开根号
# np.linalg.norm(line_point1 - line_point2)求两点间距离

x = np.array([1,2,3])
y = np.array([-1,0,1])

# np.polyfit(x,y,n)拟合n阶多项式
z = np.polyfit(x,y,1)     # [1. -2]多项式系数
p1 = np.poly1d(z)         # 得到多项式系数，按照阶数从高到低排列
print(p1)
# 调用多项式
y1 = p1([4,5])               # [2. 3.]  求对应x的各项拟合函数值
y1 = np.polyval(z,[4,5])     # 可直接使用yvals=np.polyval(z1,xxx)

a = np.array([[1,2,5,4,5],
              [2,3,4,5,7]])

d1 = np.array([0,1,2])
d2 = np.array([True,1,False])


# 逻辑与或非
print(np.logical_and(d1, d2))    # [False  True False]
mask = np.logical_and(a>2,a<5)   # [[False False False  True False]
                                 #  [False  True  True False False]

print(a[mask])      # [4 3 4]
a[mask] = 111000             # 赋值时 会对a数组对应为True的位置赋新值
# np.logical_or()
# np.logical_not()

# 数组拼接
print(np.concatenate((x, y),axis=0))    #[ 1  2  3 -1  0  1]

np.concatenate((np.array([[1,2,3],[4,5,6]]),
                np.array([[1,2,3],[4,5,6]])),axis=1)  #axis=1表示对应行的数组进行拼接
                                                #[[ 1,  2,  3, 1, 2, 3],
                                                # [ 4,  5,  6, 4, 5, 6]]
a = np.array([[1,2,5,4,5],
              [2,3,4,5,7]])

# np.squeeze删除维度（该维度长度为一时才行）
temp = np.array([[[1,2,3]],[[4,5,6]]])
np.squeeze(temp,1)   # [[1,2,3],[4,5,6]]

# 增加维度
aaa = np.array([[1,2,3,4],[5,6,7,8],[1,3,5,7],[2,4,6,8]])
b = aaa[:,None]
c = aaa[None]
print(b,b.shape)  # (4, 1, 4)
print(c,c.shape)  # (1, 4, 4)
b1 = np.expand_dims(a,axis=0)
b2 = np.expand_dims(a,axis=-1)
print(a.shape,b1.shape)  # (2, 5) (1, 2, 5)
print(a.shape,b2.shape)  # (2, 5) (2, 5, 1)

print(np.where(a==5))  # 返回每个点的索引 (array([0, 0, 1], dtype=int64), array([2, 4, 3], dtype=int64))
b = a==2
print(b)    # [[False  True False False False]
            #  [ True False False False False]]

a[b]=9
print(a)   # [[1 9 5 4 5]
           #  [9 3 4 5 7]]

# np.reshape() 可缺省一个维度，其他维度按要求 若元素个数不足以重组为矩阵则报错
a = np.array([[12,34],[56,78]])
print(a.reshape(-1,1))

aa1 = np.array([0.1288,0.123])
aa2 = np.array([3,9,123456,123])
# np.around()与np.round()等价  四舍五入保留小数点后decimals= 位 默认为0即取整   为负数时向前取整
print(np.round(aa1, decimals=0))     # [0., 0.]
print(np.around(aa1, decimals=2))    # [0.13, 0.12]
print(np.around(aa2, decimals=-1))   # [0, 10, 123460, 120]

c1 = np.array([1.1,2.6])
# np.rint(x)将x中各元素四舍五入为整数
print(np.rint(c1))    # [1., 3.]

# np.ceil()向上取整
print(np.ceil(c1))    # [2. 3.]

# np.floor()向下取整
print(np.floor(c1))   # [1. 2.]

# np.modf(x) 返回值为两个ndarray，分别为x的小数部分和x的整数部分
print(np.modf(c1))    # (array([0.1, 0.6]), array([1., 2.]))

# np.trunc(x) 返回x中的整数部分
print(np.trunc(c1))   # [1. 2.]

# np.fix(x) 返回x中相对于0的最接近的整数，如：2.9->2；-2.9->-2
print(np.fix(np.array([1.9,-3.8])))   # [ 1. -3.]
print('#'*100)
temp_1 = np.array([[3,7,5],[8,4,3],[2,4,9]])
# numpy.amin() 用于计算数组中的元素沿指定轴的最小值
print(np.amin(temp_1, 1))             # [3 3 2]

# numpy.amax() 用于计算数组中的元素沿指定轴的最大值
print(np.amax(temp_1, 0))             # [2 4 3]
print(np.amax(temp_1))                # 9  不指定轴等价于np.max()

# numpy.ptp()函数计算数组中元素最大值与最小值的差（最大值 - 最小值）
print(np.ptp(temp_1))                # 7
print(np.ptp(temp_1, 0))             # [6 3 6]

# ret = numpy.percentile(a,q) q为百分制 它使得至少有 q% 的数据项小于或等于ret，且至少有 (100-q)% 的数据项大于或等于ret
print(np.percentile(temp_1, 50))         # 4  50% 的分位数，就是 a 里排序之后的中位数
print(np.percentile(temp_1,50,axis=1))   # [5. 4. 4.]

# numpy.median()函数用于计算数组 a 中元素的中位数（中值）
print(np.median(temp_1))                 # 4
print(np.median(temp_1, axis=0))         # [3. 4. 5.]

# numpy.mean() 函数返回数组中元素的算术平均值
print(np.mean(temp_1))                 # 5
print(np.mean(temp_1, axis=0))         # [4.33333333 5.         5.66666667]

# numpy.average() 函数根据在另一个数组中给出的各自的权重计算数组中元素的加权平均值  在多维数组中，可以指定用于计算的轴
print(np.average([1,2,3], weights=[3,1,1]))   # 1.6
print(np.average([1,2,3], weights=[3,1,1], returned=True))   # (1.6, 5.0)   如果 returned 参数设为 true，则返回权重的和

# np.std() 标准差
print(np.std([1, 2, 3, 4]))     # 1.118033988749895

# np.var() 方差
print (np.var([1,2,3,4]))       # 1.25




im = Image.open('./实例练习/壁纸/001.jpg')
im = np.array(im)  # 将图片转为数组
print(im.shape)

im_red = im[:,:,0]   # 提取图片红色分量
# Image.fromarray(im_red).show()

'''
im =im1 *0.4 +im2 *0.6    #将两张图片按比例混合
im=im.astype(np.uint8)     #转为8位无符号数 以显示
Image.fromarray(im_red).show()
'''
a1 = np.random.randint(1,10,size=(3,4))
print(np.ones((1,2,3)))
a=[[1,2],
   [3,4]]

avg = np.mean(a)
print(avg)   # 2.5

avg = np.mean(a, axis=0)     # 合并行 对列求均值
print(avg)    # [2. 3.]

avg = np.mean(a, axis=1)     # 合并列 对行求均值
print(avg)    # [1.5 3.5]


b= [[5,6],
    [7,8]]

print(np.stack(b, axis=0))    # [[5,6],
                              #  [7,8]]
# 将两个数组堆叠为一个,堆叠后维度加一
c= np.stack([a,b],axis=-1)
print(c)    # [[[1 5]
            #   [2 6]]
            #  [[3 7]
            #   [4 8]]]

# 当两个数组都为一维时，axis= 0是直接堆叠
print(np.stack([[0,1,2],[7,6,5]], axis=0).astype(np.int32))   # [[0 1 2]
                                                              #  [7 6 5]]
print(np.stack([[0,1,2],[7,6,5]], axis=-1).astype(np.int32))  # [[0 7]
                                                              #  [1 6]
                                                              #  [2 5]]
# 竖向堆叠
print(np.vstack([a,b]))      # [[1 2]
                             #  [3 4]
                             #  [5 6]
                             #  [7 8]]
# 横向堆叠
print(np.hstack([a,b]))      # [[1 2 5 6]
                             #  [3 4 7 8]]
# 找最大值
print(np.max(b, axis=-1))      # [6 8]
print(np.max(b, axis=0))       # [7 8]

d = np.array([[7,5,1,4],
              [3,5,3,8],
              [2,9,2,7]])

# 找最大值所在索引
print(np.argmax(d, axis=-1))    # axis=-1 找每行最大元素的索引  [0 3 1]
print(np.argmax(d, axis=0))     # axis=0 找每列最大元素的索引    [0 2 1 1]
print(np.argmin(d, axis=0))     # 列最小元素索引 [2 0 0 0]

# 输出排序对应的索引
a13 = np.array([[8,2,4],[1,3,5]])
print(np.argsort(a13))     # [[1 2 0]
                           #  [0 1 2]]
# 改变数组形状
'''改变后数组与原数组共用同一个内存空间  故改变一个值其他数组对应值也一起改变'''
print(d.reshape((4, 3), order='C'))   # [[7 5 1]
                                      #  [4 3 5]
                                      #  [3 8 2]
                                      #  [9 2 7]]
print(d.reshape((4, 3), order='F'))   # [[7 5 2]
                                      #  [3 9 4]
                                      #  [2 1 8]
                                      #  [5 3 7]]
print(d.reshape(-1))  # 按行展开为一行[7 5 1 4 3 5 3 8 2 9 2 7]
print(d.reshape(-1,order='F'))  # 按列展开为一行[7 3 2 5 5 9 1 3 2 4 8 7]
print(d.reshape(-1,1))  # 按行展开为一列  [[7][5][1][4][3][5][3][8][2][9][2][7]]
print(d.reshape((-1,1),order='F'))  # 按列展开为一列  [[7][3][2][5][5][9][1][3][2][4][8][7]]

# 更换数组维度
print(np.transpose(d))   # [[7 3 2]    第0维和第一维、行列 互换
                         #  [5 5 9]
                         #  [1 3 2]
                         #  [4 8 7]]
d1 = np.zeros((1,2,3))
print(d1.shape)   # (1,2,3)
print(d1.transpose((1,0,2)).shape)   # (2, 1, 3)

# 创建等分数组
print(np.linspace(0, 10, 5))   # [ 0.   2.5  5.   7.5 10. ]

# 找竖线
max_pts_num = 2
a = np.array([
    [1,2,3,4,6,7,8,9],
    [6,9,4,6,37,8,43,3],
    [0,2,3,5,7,9,8,3],
])
max_h = np.argmax(a, axis=1)  # axis=1 找每行最大元素的索引  [7 6 5]
pts = np.stack([np.linspace(0, a.shape[0]-1, a.shape[0]), max_h], axis=0).astype(np.int32)
# 相当于 np.stack([[0,1,2],[7,6,5]], axis=0).astype(np.int32)
num = max_h.shape[0]   # [7,6,5]一维数组的shape[0]不代表行数  而是元素个数
if num > max_pts_num:
    used = np.linspace(0, num, max_pts_num, endpoint=False).astype(np.int32)
    used_num = used.shape[0]
else:
    used = pts[:, 1]
    used_num = num
pts = pts[:, used]
print(pts)


# 降采样
im_downsample=im[::10,::10,:]
# Image.fromarray(im_downsample).show()

# 反转图片
im_flipped = im[::-1,:,:]   # 上下翻转
# 图片裁剪
im_cropped = im[400:1400,200:900,:]

# 按比例采样
val_index = random.sample(range(0,100), k=int(0.2*100))
print(val_index)


# 解方程
import sympy
x = sympy.Symbol('x')
print(sympy.solve([3*x-18],[x]))