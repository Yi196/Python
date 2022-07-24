import cv2
import numpy as np
import matplotlib.pyplot as plt


# 载入图像
target = cv2.imread('./image/target.jpg',0)
template = cv2.imread('./image/001.jpg',0)
# 创建ORB特征点检测器
orb = cv2.ORB_create()
# 计算特征点和描述符
kp1, des1 = orb.detectAndCompute(target,None)
kp2, des2 = orb.detectAndCompute(template,None)

# BFMatching描述特征点–运行结果不精确
# 建立BFMatching匹配关系
bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING, crossCheck=True)
''' normType:NORM_L1 和 NORM_L2 更适用于 SIFT 和 SURF 描述子;
            NORM_HAMMING 和 ORB、BRISK、BRIEF 一起使用；
            NORM_HAMMING2 用于 WTA_K==3或4 的 ORB 描述子.'''
# 匹配描述符
matches = bf.match(des1, des2)    #bf.match() 和 bf.knnMatch(). 前者仅返回最佳匹配结果，后者返回 k 个最佳匹配结果.
matches = sorted(matches, key=lambda x:x.distance) #根据距离排序
# 画出匹配关系
result = cv2.drawMatches(target, kp1, template, kp2, matches[:40], None, flags=2)  #cv2.drawKeypoints() 画出关键点;
            # cv2.drawMatches() 能够画出匹配结果;cv2.drawMatchKnn()能够画出 k 个最佳匹配.
plt.imshow(result)
plt.show()


# 基于FLANN的匹配器(FLANN based Matcher)描述特征点
'''
基于FLANN的匹配器(FLANN based Matcher)
1.FLANN代表近似最近邻居的快速库。它代表一组经过优化的算法，用于大数据集中的快速最近邻搜索以及高维特征。
2.对于大型数据集，它的工作速度比BFMatcher快。
3.需要传递两个字典来指定要使用的算法及其相关参数等
对于SIFT或SURF等算法，可以用以下方法：
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
对于ORB，可以使用以下参数：
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2
'''

# 创建SIFT特征点检测器
sift = cv2.xfeatures2d.SIFT_create()
# sift = cv2.SIFT_create()   #opencv-4.5的sift算法api
# 计算特征点和描述符
kp1, des1 = sift.detectAndCompute(target,None)
kp2, des2 = sift.detectAndCompute(template,None)
# 设置Flannde参数
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE,trees=5)
searchParams= dict(checks=50)     #这个参数是searchParam,指定了索引中的树应该递归遍历的次数。值越高精度越高
flann = cv2.FlannBasedMatcher(index_params,searchParams)
matches = flann.knnMatch(des1, des2, k=2)    #knnMatch(). 返回 k 个最佳匹配结果.
# 设置好初始匹配值
matchesMask = [[0,0] for i in range(len(matches))]
for i, (m,n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        matchesMask[i] = [1,0]
# 给特征点和匹配的线定义颜色
draw_params = dict(matchColor=(0,255,0), singlePointColor=(255,0,0), matchesMask=matchesMask, flags=0)
# 画出匹配的结果
result = cv2.drawMatchesKnn(target, kp1, template, kp2, matches, None, **draw_params)
plt.imshow(result)
plt.show()



MIN_MATCH_COUNT = 10  #设置最小匹配点数
sift = cv2.xfeatures2d.SIFT_create()
# sift = cv2.SIFT_create()   #opencv-4.5的sift算法api
# 计算特征点和描述符
kp1, des1 = sift.detectAndCompute(target,None)
kp2, des2 = sift.detectAndCompute(template,None)
# 设置Flannde参数
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE,trees=5)
searchParams= dict(checks=50)     #这个参数是searchParam,指定了索引中的树应该递归遍历的次数。值越高精度越高
flann = cv2.FlannBasedMatcher(index_params,searchParams)
matches = flann.knnMatch(des1, des2, k=2)    #knnMatch(). 返回 k 个最佳匹配结果.
# 设置好初始匹配值 舍弃大于0.7的匹配
good = []
for m,n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)
# 在原图上框选出匹配到的区域
if len(good) > MIN_MATCH_COUNT:
    # 获取关键点的坐标
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    # 计算变换矩阵和MASK
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    h, w = target.shape
    # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    cv2.polylines(template, [np.int32(dst)], True, 0, 2, cv2.LINE_AA)
else:
    print( "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None
# 给特征点和匹配的线定义颜色
drawParams = dict(matchColor=(0,0,255), singlePointColor=(255,0,0), matchesMask=matchesMask, flags=2)
# 画出匹配的结果
# resultimage = cv2.drawMatches(target, kp1, template, kp2, good, None, **drawParams)
plt.imshow(template, plt.cm.gray)
plt.show()


#https://www.aiuai.cn/aifarm1636.html
