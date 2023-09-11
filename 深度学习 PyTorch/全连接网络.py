import torch
from torchvision import transforms            #图像处理
from torchvision import datasets              #加载数据集
from torch.utils.data import DataLoader       #加载数据集
import torch.nn.functional as F               #激活函数
import torch.optim as optim                   #优化器

#1 导入数据集
batch_size = 64
#图像预处理
transform = transforms.Compose([                  #将彩图转为二值图
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
    def __init__(self):
        super(Net, self).__init__()
        self.l1 = torch.nn.Linear(784, 512)
        self.l2 = torch.nn.Linear(512, 256)
        self.l3 = torch.nn.Linear(256, 128)
        self.l4 = torch.nn.Linear(128, 64)
        self.l5 = torch.nn.Linear(64, 10)

    def forward(self, x):
        x = x.view(-1,784)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))
        x = F.relu(self.l4(x))
        x = self.l5(x)
        return x

model = Net()


#3 选择损失和优化器
criterion = torch.nn.CrossEntropyLoss()   #交叉熵损失  （输入yhat， y）
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)     #实例化 优化器


#4 训练
def train(epoch):            #将训练定义为函数
    running_loss = 0.0
    for batch_idx,(x,y) in enumerate(train_loader, 0):
        optimizer.zero_grad()

        #forward + backward + updata
        y_pred = model(x)
        loss = criterion(y_pred, y)
        loss.backward()
        optimizer.step()

        running_loss +=loss.item()
        if batch_idx % 300 == 299:
            print('[%d,%5d] loss: %.3f' % (epoch+1, batch_idx+1, running_loss/300))


def test():
    correct = 0
    total = 0
    with torch.no_grad():
        for (x, y) in test_loader:
            y_pred = model(x)
            _, predicted = torch.max(y_pred.data, dim=1)
            total += y.size(0)
            correct += (predicted == y).sum().item()
    print('Accuracy on test: %d %% [%d/%d]' % (100 * correct/total, correct, total))


if __name__ == '__main__':
    for epoch in range(10):
        train(epoch)
        test()