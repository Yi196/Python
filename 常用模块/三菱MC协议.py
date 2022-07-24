from HslCommunication import MelsecMcNet
import traceback

class Plc_MC(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connect_plc()

    def connect_plc(self):
        try:
            self.melsec_net = MelsecMcNet(self.ip, self.port)
            self.melsec_net.SetPersistentConnection()  # 长连接（除去此行直接读写寄存器为短链接）
        except:
            traceback.print_exc()

    def release_plc(self):
        self.melsec_net.ConnectClose()

    def ReadInt16(self, address):
        read = self.melsec_net.ReadInt16(address)
        if read.IsSuccess:
            print('读取成功')
            return read.Content
        else:
            print('读取失败')
            raise IOError

    def WriteInt16(self, address, value):
        write = self.melsec_net.WriteInt16(address, int(value))
        if write.IsSuccess:
            print('写入成功')
        else:
            print('写入失败')
            raise IOError

if __name__ == "__main__":
    test = Plc_MC('192.168.0.100', 4999)
    test.ReadInt16('D100')
    test.WriteInt16('D101',123)
'''
    # bool read write test
    melsecNet.WriteBool("M200", True)
    printReadResult(melsecNet.ReadBool("M200"))

    # bool array read write test
    melsecNet.WriteBool("M300", [True, False, True, True, False])
    printReadResult(melsecNet.ReadBool("M300", 5))

    # int16 read write test
    melsecNet.WriteInt16("D200", 12358)
    printReadResult(melsecNet.ReadInt16("D200"))

    # int16 read write test
    melsecNet.WriteInt16("D201", -12358)
    printReadResult(melsecNet.ReadInt16("D201"))

    # uint16 read write test
    melsecNet.WriteUInt16("D202", 52358)
    printReadResult(melsecNet.ReadUInt16("D202"))

    # int32 read write test
    melsecNet.WriteInt32("D210", 12345678)
    printReadResult(melsecNet.ReadInt32("D210"))

    # int32 read write test
    melsecNet.WriteInt32("D212", -12345678)
    printReadResult(melsecNet.ReadInt32("D212"))

    # uint32 read write test
    melsecNet.WriteUInt32("D214", 123456789)
    printReadResult(melsecNet.ReadInt32("D214"))

    # int64 read write test
    melsecNet.WriteInt64("D220", 12345678901234)
    printReadResult(melsecNet.ReadInt64("D220"))

    # float read write test
    melsecNet.WriteFloat("D230", 123.456)
    printReadResult(melsecNet.ReadFloat("D230"))

    # double read write test
    melsecNet.WriteDouble("D240", 123.456789)
    printReadResult(melsecNet.ReadDouble("D240"))

    # string read write test
    melsecNet.WriteString("D250", '123456')
    printReadResult(melsecNet.ReadString("D250", 3))

    # int16 array read write test
    melsecNet.WriteInt16("D260", [123, 456, 789, -1234])
    printReadResult(melsecNet.ReadInt16("D260", 4))
'''