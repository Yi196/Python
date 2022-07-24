import numpy as np
import torch


#1 准备数据
xy = np.loadtxt('diabetes.csv.gz', delimiter=',', dtype=np.float32)    #delimiter=','指定分隔符  每行前8个元素为x 最后一个元素为y
x_data = torch.from_numpy(xy[:,:-1])
y_data = torch.from_numpy(xy[:, [-1]])


#2 建立模型
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(8,6)   #输入8维 输出6维
        self.linear2 = torch.nn.Linear(6,4)
        self.linear3 = torch.nn.Linear(4,1)
        self.activate = torch.nn.Sigmoid()    #选择激活函数此处为Sigmoid（） 可尝试多种激活函数  ReLU()（做后输出小于零置零，最后输出改为Sigmoid）

    def forward(self,x):
        x = self.activate(self.linear1(x))
        x = self.activate(self.linear2(x))
        x = self.activate(self.linear3(x))
        return x

model = Model()

'''
import torch.nn.functional as F
y_pred = F.sigmoid(self.linear(x))    #sigmoid函数 将计算出的yhat转为0到1之间 表示概率
'''


#3 选择损失和优化器
criterion = torch.nn.BCELoss(size_average=True)   #求损失（用yhat， y）
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)     #实例化 优化器


#4 训练
for epoch in range(100):
    #Forward 前馈
    y_pred = model(x_data)                #算yhat
    loss = criterion(y_pred,y_data)       #算 损失
    print(epoch, loss.item())

    #Backward 反馈
    optimizer.zero_grad()                 #梯度清零
    loss.backward()                       #反向传播

    #Updata 更新
    optimizer.step()                      #更新权重   用优化器



#Test Model
x_test = torch.Tensor([[4.0],[3.2],[1.2],[5.6],[2.3],[0.46],[7.2],[1.0]])
y_test = model(x_test)
print('y_pred = ', y_test.data)