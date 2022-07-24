from HslCommunication import MelsecMcNet
import time,pdb


class MC_Server:
    def __init__(self):
        self.ip = None
        self.port = None
        self.melsec_net = None

    def connect_plc(self):
        self.melsec_net = MelsecMcNet(self.ip, self.port)
        self.melsec_net.SetPersistentConnection()
        if self.melsec_net.ReadInt16('D100').IsSuccess:
            return True
        else:
            return False

    def release_plc(self):
        self.melsec_net.ConnectClose()

    def Read_Int16(self):
        read = self.melsec_net.ReadInt16(self.address, self.read_number)
        if read.IsSuccess:
            return read.Content
        else:
            raise IOError

    def Write_Int16(self):
        write = self.melsec_net.WriteInt16(self.address, self.write_value)
        if not write.IsSuccess:
            raise IOError


    def ReadTargetValue(self):
        if int(self.read_time) == -1:
            count = 0
            while True:
                read = self.melsec_net.ReadInt16(self.address)
                if read.IsSuccess and read.Content == self.read_value:
                    return True
                count += 1
                if count > 10000:
                    time.sleep(1)
        else:
            start = time.time()
            while True:
                read = self.melsec_net.ReadInt16(self.address)
                if read.IsSuccess:
                    if read.Content == self.read_value:
                        return True
                if (time.time() - start) > self.read_time:
                    raise TimeoutError


    def MC_Server__init__(self, tuple):
        ret_dict = {
            '0': 0,
            '1': 'Success',
            '2': [-999],
        }
        # pdb.set_trace()
        if tuple[0] != []:
            self.write_value = tuple[0][0] if len(tuple[0])==1 else tuple[0]  # 写入的值 : int或list[int]
        ip = tuple[1]                # ip
        port = tuple[2]              # 端口号
        self.address = tuple[3]      # 寄存器地址
        self.r_w = tuple[4]          # 选择读写方式：读I[nt16]、写[Int16]、轮询读
        self.read_number = None if tuple[5]==1 else tuple[5]  # 读取寄存器个数
        self.read_value = tuple[6]   # 轮询读取目标值
        self.read_time = tuple[7]    # 轮询读取等待时间


        if self.ip != ip or self.port != port:
            self.ip = ip
            self.port = port
            if not self.connect_plc():
                ret_dict['0'] = -1
                ret_dict['1'] = 'PLC链接失败'
                return ret_dict

        if self.r_w == '读[Int16]':
            try:
                ret = self.Read_Int16()
                if type(ret) == int:
                    ret_dict['2'] = [ret]
                else:
                    ret_dict['2'] = ret
                ret_dict['1'] = '读取成功'
                return ret_dict
            except:
                ret_dict['0'] = -1
                ret_dict['1'] = '读取失败'
                self.connect_plc()
                return ret_dict

        elif self.r_w == '写[Int16]':
            try:
                self.Write_Int16()
                ret_dict['1'] = '写入成功'
                ret_dict['2'] = tuple[0]
                return ret_dict
            except:
                ret_dict['0'] = -1
                ret_dict['1'] = '写入失败'
                self.connect_plc()
                return ret_dict

        elif self.r_w == '轮询读':
            try:
                self.ReadTargetValue()
                ret_dict['1'] = '获取目标值成功'
                ret_dict['2'] = [self.read_value]
                return ret_dict
            except:
                ret_dict['0'] = -1
                ret_dict['1'] = '获取目标值失败'
                if not self.melsec_net.ReadInt16('D100').IsSuccess:
                    self.connect_plc()
                return ret_dict


if __name__ == '__main__':
    mc_net = MC_Server()
    tuple = ([0], '192.168.0.250', 3000, 'D600', '轮询读', 1, 0, 2)
    ret = mc_net.MC_Server__init__(tuple)
    print(mc_net.melsec_net)
    ret = mc_net.MC_Server__init__(tuple)
    print(ret)