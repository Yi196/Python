import torch


#1 准备数据
x_data = torch.Tensor([[1.0],[2.0],[3.0]])
y_data = torch.Tensor([[2.0],[4.0],[6.0]])


#2 建立模型
class LinearModel(torch.nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = torch.nn.Linear(1,1)    ##输入1维 输出1维

    def forward(self,x):
        y_pred = self.linear(x)
        return y_pred

model = LinearModel()


#3 选择损失和优化器
criterion = torch.nn.MSELoss(size_average=False)   #求损失（用yhat， y）
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)     #实例化 优化器


#4 训练
for epoch in range(100):
    y_pred = model(x_data)                #算yhat
    loss = criterion(y_pred,y_data)       #算 损失
    print(epoch, loss.item())

    optimizer.zero_grad()                 #梯度清零
    loss.backward()                       #反向传播
    optimizer.step()                      #更新权重   用优化器



#Output weight bias
print('w = ', model.linear.weight.item())
print('b = ', model.linear.bias.item())

#Test Model
x_test = torch.Tensor([[4.0]])
y_test = model(x_test)
print('y_pred = ', y_test.data)