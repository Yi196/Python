import torch
from torch2trt import torch2trt
from torchvision.models.alexnet import alexnet
# create some regular pytorch model...
model = alexnet(pretrained=True).eval().cuda()
# create example data
x = torch.ones((1, 3, 224, 224)).cuda()
# convert to TensorRT feeding sample data as input
model_trt = torch2trt(model, [x])


# save trt model
torch.save(model_trt.state_dict(), 'alexnet_trt.engine')
# load trt model
from torch2trt import TRTModule
model_trt = TRTModule()
model_trt.load_state_dict(torch.load('alexnet_trt.engine'))


# inference
y = model(x)
y_trt = model_trt(x)
# check the output against PyTorch
print(torch.max(torch.abs(y - y_trt)))




# 画心形
# import json
#
# # with open('logic_eacheart_trash_detect.py', 'r') as f:
# #     logic_txt = json.dumps(f.read())
#
# # print(20//50)
#
#
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def lf(x, l):
#     y = x ** (2 / 3) + 0.9 * np.sqrt(3.3 - x ** 2) * np.sin(l * np.pi * x)
#     return y
#
# def show_l(numbers):
#     for n in range(numbers):
#         color = 'blue'
#         if n > 120:
#             color = 'red'
#         n = n * 0.05
#         x = np.linspace(0, 2, 1500)
#         y = [lf(i, n) for i in x]
#         plt.plot(x, y, color=color, linewidth=3)
#         plt.plot(-x, y, color=color, linewidth=3)
#         plt.xlim(-2, 2)
#
#         plt.title(f'y = x ** (2 / 3) + 0.9 * np.sqrt(3.3 - x ** 2) * np.sin({round(n, 1)} * np.pi * x)')
#         plt.ion()
#         plt.show()
#         plt.pause(0.01)
#         plt.clf()
#
# if __name__ == '__main__':
#     show_l(300)