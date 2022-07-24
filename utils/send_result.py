from HslCommunication import MelsecMcNet
import timeout_decorator


class MC_Result:
    def __init__(self):
        self.melsecResults = MelsecMcNet('192.168.0.100', 4888)
        self.melsecResults.SetPersistentConnection()

    @timeout_decorator.timeout(0.1, use_signals=False)
    def _send_result(self,ret1,ret2,ret3,ret4):
        ret_dict = {
            '0':0,
            '1':'success'
        }

        write1 = self.melsecResults.WriteInt16('D101', int(ret1))
        write2 = self.melsecResults.WriteInt16('D102', int(ret2))
        write3 = self.melsecResults.WriteInt16('D103', int(ret3))
        write4 = self.melsecResults.WriteInt16('D104', int(ret4))
        if write1.IsSuccess and write2.IsSuccess and write3.IsSuccess and write4.IsSuccess:
            return ret_dict
        else:
            raise IOError


    def send_result(self, tuple):
        try:
            ret1, ret2, ret3, ret4 = map(int,tuple)
        except:
            return {
                '0': 1015,
                '1': '参数错误'
                }
        try:
            return self._send_result(ret1,ret2,ret3,ret4)
        except:
            return {
                '0': -1,
                '1': 'connection broken',
                }


class MC_Status():
    def __init__(self):
        self.melsecStatus = MelsecMcNet('192.168.0.100', 4999)
        self.melsecStatus.SetPersistentConnection()

    @timeout_decorator.timeout(0.1, use_signals=False)
    def _is_receive(self):
        ret_dict = {
            '0': 0,
            '1': 'success',
        }

        write = self.melsecStatus.WriteInt16('D100', 200)
        if write.IsSuccess:
            return ret_dict
        else:
            raise IOError

    def is_receive(self, tuple):
        try:
            img1 = tuple[0][0]
            img2 = tuple[1][0]
            img3 = tuple[2][0]
            img4 = tuple[3][0]
        except:
            return {
                '0': 1015,
                '1': '参数错误'
            }
        try:
            return self._is_receive()
        except:
            return {
                '0': -1,
                '1': 'connection broken',
            }