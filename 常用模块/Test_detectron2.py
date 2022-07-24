import os
import get_labelme_data
import webbrowser
import threading
from tensorboard import program
from multiprocessing import Process
from distutils.dir_util import copy_tree
from detectron2 import config
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultTrainer
from detectron2.evaluation import COCOEvaluator
from detectron2.utils.logger import setup_logger

logger = setup_logger('../logs')
# os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'  # 指定GPU

class Train_Value:
    def __init__(self, is_train=True):
        self.job_name = job_name                   # 项目名称
        self.class_names = [class_names]           # 类别名称
        self.model_weights_path = model_path       # 继续训练\测试模型
        self.base_dir = base_dir                   # 模型及相关参数存放路径 TensorBorad参数
        self.trainset = [path_trainset]            # 训练集地址（可多个）
        self.valset = [path_valset]                # 验证集地址（可多个）
        self.lr = lr                               # 学习率
        self.max_iters = max_iters                 # 迭代次数
        self.resume = True                         # 是否继续训练
        self.detectron2_path = detectron2_path     # detectron2地址 用于读取backbone的yaml文件
        self.backbone = "configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml" # 选择backbone
        self.backbone_file = os.path.join(self.detectron2_path, self.backbone)
        if is_train:
            self.cfg = self.setup_cfg()
        else:
            self.cfg = self.setup_cfg_predict()


    def setup_cfg(self):
        cfg = config.get_cfg()
        cfg.merge_from_file(self.backbone_file)
        # 预训练模型权重
        cfg.MODEL.WEIGHTS = self.model_weights_path
        # batch_size
        cfg.SOLVER.IMS_PER_BATCH = 8
        # 最大迭代次数
        cfg.SOLVER.MAX_ITER = self.max_iters
        # 初始学习率
        cfg.SOLVER.BASE_LR = self.lr
        # # 使用多GPU
        # cfg.SOLVER.NUM_GPUS = 8
        # # 优化器动能
        # cfg.SOLVER.MOMENTUM = 0.9
        # # 权重衰减
        # cfg.SOLVER.WEIGHT_DECAY = 0.0001
        # cfg.SOLVER.WEIGHT_DECAY_NORM = 0.0
        # 学习率衰减倍数(每次乘0.8)
        cfg.SOLVER.GAMMA = 0.8
        # 迭代到指定次数，学习率进行衰减
        cfg.SOLVER.STEPS = (20000, 40000, 60000)
        # 在训练之前，会做一个热身运动，学习率慢慢增加至初始学习率
        cfg.SOLVER.WARMUP_FACTOR = 1.0 / 1000
        # 热身迭代次数
        cfg.SOLVER.WARMUP_ITERS = 1000
        cfg.SOLVER.WARMUP_METHOD = "linear"
        # 迭代到指定次数保存模型文件
        cfg.SOLVER.CHECKPOINT_PERIOD = 5000
        # 迭代到指定次数，进行一次评估
        cfg.TEST.EVAL_PERIOD = 5000
        # roipooling中采样region proposal个数
        cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 256
        # 类别数
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(self.class_names)
        # 模型存储路径
        cfg.OUTPUT_DIR = os.path.join(self.base_dir, self.job_name, 'model')
        # 线程数
        cfg.DATALOADER.NUM_WORKERS = 24
        # 是否裁剪用于数据增强
        cfg.INPUT.CROP.ENABLED = True
        # 过滤无标注数据
        cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS = True
        # 输入图像最大最小尺寸
        cfg.INPUT.MIN_SIZE_TRAIN = 600
        cfg.INPUT.MAX_SIZE_TRAIN = 1000
        cfg.INPUT.MIN_SIZE_TEST = 600
        cfg.INPUT.MAX_SIZE_TEST = 1000

        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
        with open(os.path.join(cfg.OUTPUT_DIR, 'label.txt'), 'w+', encoding='UTF-8') as label_file:
            for class_name in self.class_names:
                label_file.write("%s\n" % class_name)

        return cfg

    def setup_cfg_predict(self):
        cfg = config.get_cfg()
        cfg.merge_from_file(self.backbone_file)
        cfg.MODEL.WEIGHTS = self.model_weights_path
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5     # 低于50分的box过滤掉
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(self.class_names)
        cfg.INPUT.MIN_SIZE_TEST = 600
        cfg.INPUT.MAX_SIZE_TEST = 1000
        return cfg


class CocoTrainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, 'eval')
            os.makedirs(output_folder, exist_ok=True)
        return COCOEvaluator('%s' % dataset_name, cfg, False, output_folder)


class Trainer():
    def __init__(self, configs):
        super().__init__()
        self.configs = configs
        self.cfg = configs.cfg
        os.makedirs(configs.cfg.OUTPUT_DIR, exist_ok=True)
        self.job_name = configs.job_name
        self.dataset = os.path.join(self.configs.base_dir, self.job_name, 'dataset')
        self.preprocessing()
        self.process = Process(target=self.job_train)

    def merge_multiple_trainset(self):
        os.makedirs(os.path.join(self.dataset, 'train', 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.dataset, 'train', 'jsons'), exist_ok=True)
        for d in self.configs.trainset:
            print(d)
            copy_tree(os.path.join(d, 'images'), os.path.join(self.dataset, 'train', 'images'))
            copy_tree(os.path.join(d, 'jsons'), os.path.join(self.dataset, 'train', 'jsons'))

    def merge_multuple_valset(self):
        os.makedirs(os.path.join(self.dataset, 'val', 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.dataset, 'val', 'jsons'), exist_ok=True)

        for d in self.configs.valset:
            copy_tree(os.path.join(d, 'images'), os.path.join(self.dataset, 'val', 'images'))
            copy_tree(os.path.join(d, 'jsons'), os.path.join(self.dataset, 'val', 'jsons'))

    def preprocessing(self):
        self.merge_multiple_trainset()
        self.merge_multuple_valset()
        get_labelme_data.regist_dataset(os.path.join(self.dataset, 'train'), self.job_name + 'train')
        get_labelme_data.regist_dataset(os.path.join(self.dataset, 'val'), self.job_name + 'val')
        self.cfg.DATASETS.TRAIN = (self.job_name + 'train',)
        self.cfg.DATASETS.TEST = (self.job_name + 'val',)
        MetadataCatalog.get(self.job_name + 'train').thing_classes = self.configs.class_names
        MetadataCatalog.get(self.job_name + 'val').thing_classes = self.configs.class_names

    def start_tensorboard(self):
        tb = program.TensorBoard()
        tb.configure(argv=[None, '--logdir', self.configs.base_dir, '--bind_all'])
        url = tb.launch()
        webbrowser.open('http://localhost:' + url.split(':')[-1])

    def job_train(self):
        trainer = CocoTrainer(self.cfg)
        trainer.resume_or_load(resume=self.configs.resume)
        trainer.train()

    def start_train(self):
        self.process.start()

    def stop_train(self):
        self.process.terminate()

if __name__ == '__main__':
    config = Train_Value()
    train = Trainer(config)
    train.start_train()
    # tb = threading.Thread(target=train.start_tensorboard)
    # tb.start()