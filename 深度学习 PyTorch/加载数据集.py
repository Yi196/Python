import torch
import numpy as np
from torch.utils.data import Dataset,DataLoader


#1 准备数据
class MinDataset(Dataset):                                       #定义数据集
    def __init__(self,filepath):
        xy = np.loadtxt(filepath, delimiter=',', dtype=np.float32)
        self.len = xy.shape[0]
        self.x_data = torch.from_numpy(xy[:,:-1])
        self.y_data = torch.from_numpy(xy[:,[-1]])

    def __getitem__(self, index):                                 #添加索引
        return self.x_data[index], self.y_data[index]

    def __len__(self):                                            #添加返回数据个数 的函数
        return self.len

dataset = MinDataset('file')                 #文件地址以读入数据
train_loader = DataLoader(dataset=dataset,   #传入数据集
                          batch_size=32,     #每次训练的样本数
                          shuffle=True,      #是否在每次迭代后打乱数据集的顺序
                          num_workers=2)     #用于并行的进程数


#2 建立模型
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(8,6)   #输入8维 输出6维
        self.linear2 = torch.nn.Linear(6,4)
        self.linear3 = torch.nn.Linear(4,1)
        self.activate = torch.nn.Sigmoid()    #选择激活函数此处为Sigmoid（输出值为0-1） 可尝试多种激活函数  ReLU()（输出小于零置零，最后输出改为Sigmoid）

    def forward(self,x):
        x = self.activate(self.linear1(x))
        x = self.activate(self.linear2(x))
        x = self.activate(self.linear3(x))
        return x

model = Model()


#3 选择损失和优化器
criterion = torch.nn.BCELoss(size_average=True)   #求损失（用yhat， y）
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)     #实例化 优化器


#4 训练
#if __name__ == '__main__':   #windows下避免多进程出错
len1 = len(dataset)
for epoch in range(100):
    for i,(x,y) in enumerate(train_loader,0):     #方便使用Mini—Batch的数据类型:一次加载部分打乱顺序的训练集， 该循环完成一周，训练集迭代一次
        #Forward 前馈
        y_pred = model(x)                     #算yhat
        loss = criterion(y_pred,y)            #算 损失
        print(epoch*len1+i, loss.item())      #epoch*len1+i 表示迭代次数

        #Backward 反馈
        optimizer.zero_grad()                 #梯度清零
        loss.backward()                       #反向传播

        #Updata 更新
        optimizer.step()                      #更新权重   用优化器

