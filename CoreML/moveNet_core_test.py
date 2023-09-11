import os,cv2,time
import numpy as np
from PIL import Image
import coremltools as ct
import tensorflow as tf
from human_keypoint_coco import CocoColors, SKELETON

def img_bgr_processing(img_bgr, input_size=256):
    img_rgb = img_bgr[:, :, [2, 1, 0]]
    img_h, img_w, _ = img_rgb.shape
    pad_image = np.zeros((input_size, input_size, 3), dtype=np.uint8)
    r = min(input_size / img_h, input_size / img_w)

    resize_img = cv2.resize(img_rgb, (int(img_w * r), int(img_h * r)))
    pad_image[0:int(img_h * r), 0:int(img_w * r), :] = resize_img
    # pad_image = pad_image / 127.5 - 1
    # pad_image = np.transpose(pad_image, (2, 0, 1))

    img_nhwc = pad_image[None,].astype(np.float32)
    print(img_nhwc.shape)

    return img_nhwc, r



# model = ct.models.MLModel('../weights/movenet_singlepose.mlmodel')           # fps: 335
# print(model.input_description)
# im = cv2.imread('../weights/test.jpg')
# input, r = img_bgr_processing(img_bgr=im, input_size=256)


model = ct.models.MLModel('../weights/movenet_multipose.mlmodel')           # fps: 79    精度损失: 0.005
print(model.input_description)
im = cv2.imread('../weights/test.jpg')
img_draw = im.copy()
input, r = img_bgr_processing(img_bgr=im, input_size=416)


for _ in range(1000):
    s = time.time()
    y = model.predict({'input': input})
    print('fps: ', 1 / (time.time() - s))
print(y)


t_h = 416 / r
t_w = 416 / r

kpt_lst = []
person_bbox = []
person_score = []

for kpts in y['Identity'][0]:
    person_score.append(kpts[-1])
    person_bbox.append(np.asarray([kpts[-5] * t_h, kpts[-4] * t_w, kpts[-3] * t_h, kpts[-2] * t_w]))    # [ymin, xmin, ymax, xmax]

    k_lst = []
    for i in range(17):
        k_lst.append(([kpts[i * 3] * t_h, kpts[i * 3 + 1] * t_w, kpts[i * 3 + 2]]))

    kpt_lst.append(np.asarray(k_lst))

for idx_person, kpts in enumerate(kpt_lst):
    if person_score[idx_person] > 0.2:
        for i in range(len(SKELETON)):
            kpt_a, kpt_b = SKELETON[i][0], SKELETON[i][1]
            if kpts[kpt_a][2] > 0.1:
                x_a, y_a = kpts[kpt_a][1], kpts[kpt_a][0]
                cv2.circle(img_draw, (int(x_a), int(y_a)), 6, CocoColors[i], -1)
            if kpts[kpt_b][2] > 0.1:
                x_b, y_b = kpts[kpt_b][1], kpts[kpt_b][0]
                cv2.circle(img_draw, (int(x_b), int(y_b)), 6, CocoColors[i], -1)
            if kpts[kpt_a][2] > 0.1 and kpts[kpt_b][2] > 0.1:
                cv2.line(img_draw, (int(x_a), int(y_a)), (int(x_b), int(y_b)), CocoColors[i], 2)

        cv2.rectangle(img_draw, (int(person_bbox[idx_person][1]), int(person_bbox[idx_person][0])),
                      (int(person_bbox[idx_person][3]), int(person_bbox[idx_person][2])), CocoColors[idx_person], 2)

cv2.imshow(' ', img_draw)
cv2.waitKey(0)