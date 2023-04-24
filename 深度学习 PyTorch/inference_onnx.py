import cv2
import numpy as np
import onnxruntime


COCO_KEYPOINT_INDEXES = {
    0: 'nose',
    1: 'left_eye',
    2: 'right_eye',
    3: 'left_ear',
    4: 'right_ear',
    5: 'left_shoulder',
    6: 'right_shoulder',
    7: 'left_elbow',
    8: 'right_elbow',
    9: 'left_wrist',
    10: 'right_wrist',
    11: 'left_hip',
    12: 'right_hip',
    13: 'left_knee',
    14: 'right_knee',
    15: 'left_ankle',
    16: 'right_ankle'
}


SKELETON = [
    [1, 3], [1, 0], [2, 4], [2, 0], [0, 5], [0, 6], [5, 7], [7, 9], [6, 8],
    [8, 10], [5, 11], [6, 12], [11, 12], [11, 13], [13, 15], [12, 14], [14, 16]
]


CocoColors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0],
              [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255],
              [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]


NUM_KPTS = 17


class MoveNet_onnx(object):
    def __init__(self, model_path):
        self.model = onnxruntime.InferenceSession(model_path)
        # self.model = onnxruntime.InferenceSession(model_path, providers=['CUDAExecutionProvider'])    # 使用GPU加速
        self.input_name = self.model.get_inputs()[0].name
        self.output_name = self.model.get_outputs()[0].name

    def pre_processing(self, box, image, input_h, input_w, ratio=1.02):
        h_ori, w_ori, _ = image.shape
        x1, y1 = max(int(box[0] / ratio), 0), max(int(box[1] / ratio), 0)
        x2, y2 = int(min(box[2] * ratio, w_ori)), int(min(box[3] * ratio, h_ori))
        box_image = image[y1:y2, x1:x2]
        img_h, img_w, _ = box_image.shape

        pad_image = np.zeros((input_h, input_w, 3), dtype=np.uint8)
        r = min(input_h / img_h, input_w / img_w)
        resize_img = cv2.resize(box_image, (int(img_w * r), int(img_h * r)))
        pad_image[0:int(img_h * r), 0:int(img_w * r)] = resize_img

        pad_image = pad_image / 127.5 - 1
        input_image = np.transpose(pad_image, (2, 0, 1))
        img_nchw = input_image[None, ].astype(np.float32)
        top_left_corner = (x1, y1)

        return img_nchw, r, top_left_corner

    def post_process(self, outputs, ratio, top_left_corner):
        outputs[..., 0] = outputs[..., 0] * 256 / ratio + top_left_corner[1]
        outputs[..., 1] = outputs[..., 1] * 256 / ratio + top_left_corner[0]
        outputs = outputs.reshape(1, 17, 3)
        return outputs

    def draw_img(self, img, keypoints, threshold=0.25):
        """draw the keypoints and the skeletons.
        :params keypoints: the shape should be equal to [17,2]
        :params img:
        """
        assert keypoints.shape == (NUM_KPTS, 3)
        for i in range(len(SKELETON)):
            kpt_a, kpt_b = SKELETON[i][0], SKELETON[i][1]
            if keypoints[kpt_a][2] > threshold:
                x_a, y_a = keypoints[kpt_a][1], keypoints[kpt_a][0]
                cv2.circle(img, (int(x_a), int(y_a)), 6, CocoColors[i], -1)

            if keypoints[kpt_b][2] > threshold:
                x_b, y_b = keypoints[kpt_b][1], keypoints[kpt_b][0]
                cv2.circle(img, (int(x_b), int(y_b)), 6, CocoColors[i], -1)

            if keypoints[kpt_a][2] > threshold and keypoints[kpt_b][2] > threshold:
                cv2.line(img, (int(x_a), int(y_a)), (int(x_b), int(y_b)), CocoColors[i], 2)

        return img

    def detect(self, img_bgr, pred_box):
        img_nchw, r, top_left_corner = self.pre_processing(pred_box, img_bgr, 256, 256, ratio=1)

        outputs = self.model.run([self.output_name], {self.input_name: img_nchw})[0]

        self.post_process(outputs, r, top_left_corner)

        return outputs[0][0]


if __name__ == '__main__':
    model = MoveNet_onnx(r'../weights/movenet_sim.onnx')
    img_bgr = cv2.imread(r'../weights/test.jpg')

    kpt = model.detect(img_bgr, [0, 0, 9999, 9999])
    print(kpt)

    img_draw = model.draw_img(img_bgr, kpt, 0.1)
    cv2.imshow(' ', img_draw)
    cv2.waitKey(0)