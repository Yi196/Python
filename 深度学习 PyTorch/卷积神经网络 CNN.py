import torch
from torchvision import transforms            #图像处理
from torchvision import datasets              #加载数据集
from torch.utils.data import DataLoader       #加载数据集
import torch.nn.functional as F               #激活函数
import torch.optim as optim                   #优化器

#1 导入数据集
batch_size = 1       #每次输入样本个数

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307, ), (0.3081, ))  #均值、标准差
])

train_dataset = datasets.MNIST(root='./dataset/mnist/',
                               train=True,
                               download=True,
                               transform=transform)
train_loader = DataLoader(train_dataset,
                          shuffle=True,
                          batch_size=batch_size)

test_dataset = datasets.MNIST(root='./dataset/mnist/',
                               train=False,
                               download=True,
                               transform=transform)
test_loader = DataLoader(test_dataset,
                          shuffle=False,
                          batch_size=batch_size)


#模型
class Net(torch.nn.Module):
    def __init__(self, in_channels):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels, 10, kernel_size=5 )    #卷积层    参数：输入通道1； 输出通达10； 卷积核大小5X5
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5 )
        self.pooling = torch.nn.MaxPool2d(2)                   #池化层    最大池化：参数：卷积核2X2，且步长为2降采样（即输入24X24，输出12X12 通道数不变）
        self.fc = torch.nn.Linear(320, 10)                     #最后转为输入320，输出10的全连接网络

    def forward(self, x):
        batch_size = x.size(0)
        x = F.relu(self.pooling(self.conv1(x)))    #先卷积 再池化 再用激活函数Relu（）
        x = F.relu(self.pooling(self.conv2(x)))
        x = x.view(batch_size, -1)                 #转为全连接网络所需要的输入格式
        x = self.fc(x)                             #转为全连接网络
        return x

model = Net(in_channels=1)   #输入通道数为1
#使用GPU 显卡计算
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')   #若有显卡，则使用显卡
model.to(device)  #将模型迁移至显卡


#3 选择损失和优化器
criterion = torch.nn.CrossEntropyLoss()   #交叉熵损失  （输入yhat， y）
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5 )     #实例化 优化器


#4 训练
def train(epoch):            #将训练定义为函数
    running_loss = 0.0
    for batch_idx, (x,y) in enumerate(train_loader,0):
        x, y = x.to(device), y.to(device)   #将数据输入、输出都迁移到显卡上
        optimizer.zero_grad()

        #forward + backward + updata
        y_pred = model(x)
        loss = criterion(y_pred, y)
        loss.backward()
        optimizer.step()

        running_loss +=loss.item()
        if batch_idx % 300 == 299:
            print('[%d,%5d] loss: %.3f' % (epoch+1, batch_idx+1, running_loss/300 ))


def test():
    correct = 0
    total = 0
    with torch.no_grad():
        for (x, y) in test_loader:
            x, y = x.to(device), y.to(device)  # 将数据输入、输出都迁移到显卡上
            y_pred = model(x)
            _, predicted = torch.max(y_pred.data, dim=1)
            total += y.size(0)
            correct += (predicted == y).sum().item()
    print('Accuracy on test: %d %% [%d/%d]' % (100 * correct/total, correct, total))


if __name__ == '__main__':
    for epoch in range(10):
        train(epoch)
        test()