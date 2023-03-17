# 1
# os.system()
# 优点：简单易理解，能够返回执行命令的成功失败，返回0是成功，非0是失败
# 缺点：会造成堵塞，无法设置超时，不能输出控制台的结果


# 2
# os.popen()
# 优点：简单易理解，能够输出控制台的结果
# 缺点：无法获取命令是否执行成功，不清楚是否能够设置超时


# 3
# subprocess.check_output()
# 优点：简单易理解，能够输出控制台的结果，能够知道是否超时
# 缺点：需要在命令执行完成才会抛出超时异常


# 4
# subprocess.Popen()
# 优点：能够输出控制台的结果，能够进行超时的控制

import os
import signal
import subprocess
import platform


def run_cmd(cmd_string, timeout=20):
    print("命令为：" + cmd_string)
    p = subprocess.Popen(cmd_string, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, close_fds=True,
                         start_new_session=True)

    format = 'utf-8'
    if platform.system() == "Windows":
        format = 'gbk'

    try:
        (msg, errs) = p.communicate(timeout=timeout)
        ret_code = p.poll()
        if ret_code:
            code = 1
            msg = "[Error]Called Error ： " + str(msg.decode(format))
        else:
            code = 0
            msg = str(msg.decode(format))
    except subprocess.TimeoutExpired:
        # 注意：不能只使用p.kill和p.terminate，无法杀干净所有的子进程，需要使用os.killpg
        p.kill()
        p.terminate()
        os.killpg(p.pid, signal.SIGTERM)

        # 注意：如果开启下面这两行的话，会等到执行完成才报超时错误，但是可以输出执行结果
        # (outs, errs) = p.communicate()
        # print(outs.decode('utf-8'))

        code = 1
        msg = "[ERROR]Timeout Error : Command '" + cmd_string + "' timed out after " + str(timeout) + " seconds"
    except Exception as e:
        code = 1
        msg = "[ERROR]Unknown Error : " + str(e)

    return code, msg

# https://blog.csdn.net/jiandanokok/article/details/103644902