import subprocess

#用默认音乐播放器打开MP3文件
proc = subprocess.Popen(
    ['start',                #Windows下start； MAC下open；Linux下用see
     '文件路劲.mp3'],
    shell=True               #windows下要加此参数
)
proc.communicate()

#调用程序解压文件
proc = subprocess.Popen(
    [
        r'调用的解压程序路径.exe',
        'x',         #代表解压
        '要解压文件的路径',
        '文件解压到的地址',
        '-aoa'   #覆盖模式
    ],
    shell=True
)

proc.communicate()