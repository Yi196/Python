from pyModbusTCP.server import ModbusServer
import time
import traceback
from plcModule import config


class ModbusServerClass(object):
    def __init__(self, address1=0, address_value1=(200, 300, 400), address2=3, address_value2=(404, 505, 606)):
        self.ip = config['plc_params']['IP']     # 此处应和本机IP保持一致或为"localhost"
        self.port = config['plc_params']['tcpPort']
        self.address1 = address1
        self.address2 = address2
        self.address_value1 = list(map(int, address_value1))
        self.address_value2 = list(map(int, address_value2))
        try:
            self.server = ModbusServer(host=self.ip, port=self.port, no_block=True)

            # holding register能读能写,input register能读不能写
            self.server.data_bank.set_holding_registers(self.address1,self.address_value1)
            self.server.data_bank.set_holding_registers(self.address2,self.address_value2)

            if not self.server.is_run:
                self.server.start()
            print('Modbus服务器开启成功！', '\n', f'{config["plc_params"]}')
        except:
            traceback.print_exc()
            print('Modbus服务器开启失败！')

    def get_address_valus(self, address=None, number=None):
        if address == None:
            address = self.address1
        if number == None:
            number = len(self.address_value1)
        return self.server.data_bank.get_holding_registers(address, number=number)


if __name__ == '__main__':
    modbus_server = ModbusServerClass()
    while True:
        values = modbus_server.get_address_valus()
        print(values)
        time.sleep(1)
    # print('Modbus.server.is_run:', modbus_server.server.is_run)