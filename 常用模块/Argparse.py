import argparse

#实例化命令行解析器
parser = argparse.ArgumentParser(description='Tish is a demo about argparse!')
#添加位置参数(位置参数不可缺省)
parser.add_argument('x',type=int ,help='x is a integer')
#添加可选参数
parser.add_argument("-v", "--verbose",action="store_true")   #'-v'与'--verbose'等价  action="store_true"表示这是一个标志位，不需要输入值，有'-v'表示为True，没有为False
parser.add_argument("-z",action="count")   #action="count"表示会统计输入的‘-z’数量
parser.add_argument('--num_classes', type=int, default=5, help='num_classes of output')

args = parser.parse_args()

print('x is ',args.x)
if args.verbose:
    print('verbosity turned on')

if args.z == 2:
    print('-z input 2 times')

print('num_classes is ',args.num_classes)


'''
python Argparse.py 3 --verbose -zz --num_classes 8
'''