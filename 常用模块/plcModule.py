# from configs.config import config
from pyModbusTCP.client import ModbusClient
import logging_info
import modbus
import os
import time
import traceback


_DEPLOY = False
config = {
    'plc_params': {
        'IP':'192.168.0.250' if _DEPLOY else "localhost",
        'tcpPort':5001 if _DEPLOY else 502
    },
    #通讯及拍照地址， value=100进行拍照，拍照完写0。 给检测结果时写200作为标识位。
    'grab_addr': 0,
    'log_dir': r'../logs/'
}


class PlcModule():
    def __init__(self):
        self.logger = logging_info.set_logger(config['log_dir'], os.path.basename(__file__))
        self.logger.info('Test to connect pclModule: '+ str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.logger.info(config['plc_params'])

        time_start = time.time()
        self.connectPlc()
        print(time.time() - time_start)

    def releasePlc(self):
        self.plc_client.close()

    def connectPlc(self):
        try:
            client = ModbusClient()
            client.port(config['plc_params']['tcpPort'])
            client.host(config['plc_params']['IP'])
            a = 5
            while a:
                if not client.is_open():
                    if not client.open():
                        self.logger.error(f"connect to PLC error!   TEST:{a}")
                        time.sleep(0.5)
                    else:
                        break
                else:
                    break
                a -= 1

            self.plc_client = client

            if not self.plc_client.is_open():
                self.logger.error("connect to PLC error")
            else:
                self.logger.info("link PLC successful")

        except Exception:
            traceback.print_exc()

    def createOncePlcTri(self):
        if self.plc_client is None:
            self.connectPlc()
        l_value = 100
        bRet = self.plc_client.write_single_register(config['grab_addr'], l_value)
        if bRet:
            return True
        else:
            return False

    def getTriOnceStatus(self):
        if self.plc_client is None:
            self.connectPlc()
        regs = self.plc_client.read_holding_registers(config['grab_addr'], 1)
        # print(str(regs))
        noSignalNum = 0
        while regs == None:
            regs = self.plc_client.read_holding_registers(config['grab_addr'], 1)
            if regs == None:
                noSignalNum+=1
                if noSignalNum == 5:
                    self.logger.error('canot read the value of plcAddr!')
                    return False
                time.sleep(0.01)

        if regs[0]==100:
            print(str(regs))
            return True
        else:
            return False

    def setTriStatusZero(self):
        if self.plc_client is None:
            self.connectPlc()
        l_value = 0
        bRet = self.plc_client.write_single_register(config['grab_addr'], l_value)
        if bRet:
            return True
        else:
            return False

    def sendDetectResults2Plc(self, rlts):
        if self.plc_client is None:
            self.connectPlc()
        bRet = self.plc_client.write_multiple_registers(config['grab_addr'], rlts)
        if not bRet:
            self.logger.error('send values: ', rlts)
            self.logger.error('send detect_results failed! **write failed!')
        time.sleep(0.001)

    def run(self):
        if self.plc_client is None:
            self.connectPlc()

        data = 33
        data1 = 36
        while True:
            print('sending data to PLC')
            print('cur_data = %d'%data)

            bRet = self.plc_client.is_open()
            print('plc is open: '+str(bRet))

            regs = self.plc_client.read_coils(config['grab_addr'], 16)
            if regs:
                print("reg ad #0 to 1: " + str(regs))

            regs_6 = self.plc_client.read_holding_registers(config['grab_addr'], 1)
            if regs_6:
                print("reg ad #0 to 1: " + str(regs_6))

            output_value = data
            bRet = self.plc_client.write_single_register(config['grab_addr'], output_value)
            if not bRet:
                print('write modbusTCP failed!')

            output_value = [data, data+1, data+2, data+3, data+4, data+5, data+6]
            bRet = self.plc_client.write_multiple_registers(config['grab_addr'], output_value)
            if not bRet:
                print('write modbusTCP failed!')
            time.sleep(0.001)

            regs = self.plc_client.read_holding_registers(config['grab_addr'], 2)
            if regs:
                print("reg ad #0 to 1: " + str(regs))

            regs_6 = self.plc_client.read_holding_registers(config['grab_addr'], 9)
            if regs_6:
                print("reg ad #0 to 1: " + str(regs_6))

            data+=3


if __name__ == '__main__':
    test = PlcModule()
    # test.run()