import numpy as np
import cv2 as cv

#读取视频
cap = cv.VideoCapture('./image/001.mp4')   #也可获取一个摄像头

#判断视频是否读取成功
while (cap.isOpened()):
    #获取每一帧图像
    ret,fram = cap.read()    #获取一帧图像 返回值 ret获取成功为True  fram获取到的一帧图片
    if ret == True:
        cv.imshow('fram',fram)
    if cv.waitKey(25)&0xff==ord('q'):   #表示每25毫秒刷新一帧  按q退出
        break

#查
print(cap.get(0))  #图像位置
print(cap.get(1))  #当前帧位置
print(cap.get(2))  #文件相对位置
print(cap.get(3))  #帧宽度
print(cap.get(4))  #帧高度
print(cap.get(5))  #帧率
print(cap.get(6))  #编解码器四字符代码
print(cap.get(7))  #视频总帧数
fram_width = int(cap.get(3))
fram_hight = int(cap.get(4))
#修改
#cap.set(5,60)

#保存
out = cv.VideoWriter('./image/002.avi',cv.VideoWriter_fourcc('D','I','V','X'),10,(fram_width,fram_hight))
           #参数为     保存地址               编解码器四字符代码 注意不同操作系统不同   帧率     帧大小（宽，高）
while True:
    ret,fram = cap.read()
    if ret==True:
        out.write(fram)
    else:
        break


#释放资源
cap.release()
out.release()
cv.destroyAllWindows()
