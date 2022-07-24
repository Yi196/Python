import sys
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtGui import QIcon  #显示图标

class FirstWindow(QMainWindow):
    def __init__(self):
        super(FirstWindow, self).__init__()

        #设置主窗口的标题
        self.setWindowTitle('第一个主窗口')

        #设置窗口尺寸
        self.resize(400,300)

        #设置状态栏
        self.status = self.statusBar()
        self.status.showMessage('只存在五秒的信息',5000)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #设置图标
    app.setWindowIcon(QIcon('./image/001.jpg'))

    main = FirstWindow()
    main.show()
    sys.exit(app.exec_())
