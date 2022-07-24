import sys
import ui_03

from PyQt5.QtWidgets import QApplication,QMainWindow
from qt_material import apply_stylesheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()

    apply_stylesheet(app, theme='dark_teal.xml')

    ui = ui_03.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
