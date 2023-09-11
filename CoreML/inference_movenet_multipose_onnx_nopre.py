import time
import cv2
import numpy as np
import onnxruntime
from human_keypoint_coco import *


class MoveNet_onnx(object):
    def __init__(self, model_path, input_h=416, input_w=416):
        self.input_h = input_h
        self.input_w = input_w

        self.model = onnxruntime.InferenceSession(model_path, providers=['CUDAExecutionProvider'])
        self.input_name = self.model.get_inputs()[0].name
        self.output_name = self.model.get_outputs()[0].name

    def pre_processing(self, img_bgr):
        img_rgb = img_bgr[:, :, [2, 1, 0]]
        img_h, img_w, _ = img_rgb.shape
        pad_image = np.zeros((self.input_h, self.input_w, 3), dtype=np.uint8)
        r = min(self.input_h / img_h, self.input_w / img_w)

        resize_img = cv2.resize(img_rgb, (int(img_w * r), int(img_h * r)))
        pad_image[0:int(img_h * r), 0:int(img_w * r), :] = resize_img
        pad_image = pad_image / 127.5 - 1
        pad_image = np.transpose(pad_image, (2, 0, 1))

        img_nhwc = pad_image[None, ].astype(np.float32)

        return img_nhwc, r

    def post_process(self, outputs, ratio):
        '''

        :param outputs:
        :param ratio:
        :return: kpt_lst:六人关键点列表， person_bbox:六人bbox， person_score:六人置信度
        '''
        t_h = self.input_h / ratio
        t_w = self.input_w / ratio

        kpt_lst = []
        person_bbox = []
        person_score = []

        for kpts in outputs[0]:
            person_score.append(kpts[-1])
            person_bbox.append(np.asarray([kpts[-5] * t_h, kpts[-4] * t_w, kpts[-3] * t_h, kpts[-2] * t_w]))    # [ymin, xmin, ymax, xmax]

            k_lst = []
            for i in range(17):
                k_lst.append(([kpts[i * 3] * t_h, kpts[i * 3 + 1] * t_w, kpts[i * 3 + 2]]))

            kpt_lst.append(np.asarray(k_lst))

        return kpt_lst, person_bbox, person_score

    def draw_img(self, img, kpt_lst, person_bbox, person_score, thresh_person=0.3, thresh_kpt=0.2):
        for idx_person, kpts in enumerate(kpt_lst):
            if person_score[idx_person] > thresh_person:
                for i in range(len(SKELETON)):
                    kpt_a, kpt_b = SKELETON[i][0], SKELETON[i][1]
                    if kpts[kpt_a][2] > thresh_kpt:
                        x_a, y_a = kpts[kpt_a][1], kpts[kpt_a][0]
                        cv2.circle(img, (int(x_a), int(y_a)), 6, CocoColors[i], -1)
                    if kpts[kpt_b][2] > thresh_kpt:
                        x_b, y_b = kpts[kpt_b][1], kpts[kpt_b][0]
                        cv2.circle(img, (int(x_b), int(y_b)), 6, CocoColors[i], -1)
                    if kpts[kpt_a][2] > thresh_kpt and kpts[kpt_b][2] > thresh_kpt:
                        cv2.line(img, (int(x_a), int(y_a)), (int(x_b), int(y_b)), CocoColors[i], 2)

                cv2.rectangle(img, (int(person_bbox[idx_person][1]), int(person_bbox[idx_person][0])),
                              (int(person_bbox[idx_person][3]), int(person_bbox[idx_person][2])), CocoColors[idx_person], 2)

        return img

    def detect(self, img_bgr):
        img_nhwc, r = self.pre_processing(img_bgr)
        outputs = self.model.run([self.output_name], {self.input_name: img_nhwc})[0]

        kpt_lst, person_bbox, person_score = self.post_process(outputs, r)

        return kpt_lst, person_bbox, person_score


if __name__ == '__main__':
    model = MoveNet_onnx(r'../weights/movenet_multipose_416_sim_nopre.onnx', input_h=416, input_w=416)

    img_bgr = cv2.imread('../weights/test.jpg')
    # kpt_lst, person_bbox, person_score = model.detect(img_bgr)
    # print(kpt_lst, person_bbox, person_score)

    for _ in range(1000):
        s = time.time()
        y = model.detect(img_bgr)              # fps: 17
        print('fps: ', 1 / (time.time() - s))

    #
    # img_draw = model.draw_img(img_bgr, kpt_lst, person_bbox, person_score)
    # cv2.imshow(' ', img_draw)
    # cv2.waitKey(0)

    # # video_path = r'rtsp://admin:tp123456@192.168.8.166:554/Streaming/Channels/101'
    # video_path = r'/home/mafneg/桌面/算法/挥手-江南豪园-球机_20230531.mp4'
    # cap = cv2.VideoCapture(video_path)
    #
    # ret, frame = cap.read()
    # while ret:
    #     kpt_lst, person_bbox, person_score = model.detect(frame)
    #
    #     img_draw = model.draw_img(frame, kpt_lst, person_bbox, person_score)
    #     cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    #     cv2.imshow('frame', img_draw)
    #     cv2.waitKey(0)
    #
    #     ret, frame = cap.read()


