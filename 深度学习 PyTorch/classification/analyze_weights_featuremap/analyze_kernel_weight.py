import torch
from alexnet_model import AlexNet
from resnet_model import resnet34
import matplotlib.pyplot as plt
import numpy as np


# create model
# model = AlexNet(num_classes=5)
model = resnet34(num_classes=5)
# load model weights
model_weight_path = "../ResNet/resNet34.pth"  # "./AlexNet.pth"
model.load_state_dict(torch.load(model_weight_path))
print(model)

for value in model.state_dict().values():
    print(value.numpy().shape)  # [kernel_number, kernel_channel, kernel_height, kernel_width]

weights_keys = model.state_dict().keys()
for key in weights_keys:
    # remove num_batches_tracked para(in bn)
    if "conv" not in key:
        continue
    # [kernel_number, kernel_channel, kernel_height, kernel_width]
    weight_t = model.state_dict()[key].numpy()

    # read a kernel information
    k = weight_t[0, :, :, :]
    print(k)

    # calculate mean, std, min, max
    weight_mean = weight_t.mean()
    weight_std = weight_t.std(ddof=1)
    weight_min = weight_t.min()
    weight_max = weight_t.max()
    print("mean is {}, std is {}, min is {}, max is {}".format(weight_mean,
                                                               weight_std,
                                                               weight_max,
                                                               weight_min))

    # plot hist image
    plt.close()
    weight_vec = np.reshape(weight_t, [-1])
    plt.hist(weight_vec, bins=50)
    plt.title(key)
    plt.show()

