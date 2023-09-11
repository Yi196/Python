import time

import torch
import cv2
import numpy as np
import coremltools as ct
from PIL import Image
import random


def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y



model = ct.models.MLModel('yolov7-nms.mlmodel')


im = cv2.imread('../weights/test.jpg')
im = cv2.resize(im, (640, 640))
img_draw = im.copy()

h, w, ch = im.shape

im = Image.fromarray((im).astype('uint8'))

for _ in range(1000):
    s = time.time()
    y = model.predict({'image': im})
    print('fps: ', 1 / (time.time() - s))
# print(y)


if 'confidence' in y:
     box = xywh2xyxy(y['coordinates'] * [[w, h, w, h]])  # xyxy pixel
     conf, cls = y['confidence'].max(1), y['confidence'].argmax(1).astype(np.int8)
     yp = np.concatenate((box, conf.reshape(-1, 1), cls.reshape(-1, 1)), 1)
else:
     k = 'var_' + str(sorted(int(k.replace('var_', '')) for k in y)[-1])  # output key
     yp = y[k]  # output

print(yp)



def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


for x in yp:
    plot_one_box(x, img_draw)

cv2.imshow(' ', img_draw)
cv2.waitKey(0)