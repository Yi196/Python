import time
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from openpyxl import load_workbook
import pandas as pd
import os


class Save:

    def __init__(self):
        self.ui = QUiLoader().load('./UI/ui_05.ui')

        self.ui.save_button.clicked.connect(self.save2excel)
        self.result_count_dict={
            '总数':100,
            '缺陷':20,
            '良品率':0.8,
            '缺陷1':2,
            '缺陷2':8,
            '缺陷3':10,
        }
        self.save_path = '../RBF694.xlsx'
        self.save_sheet = 'RBF694'

    def save2excel(self):
        dict_1 = {'时间':time.strftime('%Y/%m/%d %H:%M:%S',time.localtime())}
        dict_2 = self.result_count_dict
        save_dict = dict(dict_1,**dict_2)  #合并字典
        # print(save_dict)
        if not os.path.exists(self.save_path):
            df_1 = pd.DataFrame(save_dict, index=[0])
            df_1.to_excel(self.save_path,sheet_name=self.save_sheet,index=None)
        else:
            df = pd.read_excel(self.save_path,sheet_name=self.save_sheet)
            df_rows = df.shape[0]
            book = load_workbook(self.save_path)
            writer = pd.ExcelWriter(self.save_path, engine='openpyxl')
            writer.book = book
            writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            df_1= pd.DataFrame(save_dict,index=[0])
            df_1.to_excel(writer, sheet_name=self.save_sheet, startrow=df_rows + 1, index=False,header=False)  # 将数据写入excel中的'RBF694'表,从第一个空行开始写
            writer.save()  # 保存
            writer.close()

app = QApplication([])
app.setWindowIcon(QIcon('./image/001.jpg'))
stats = Save()
stats.ui.show()
app.exec_()

