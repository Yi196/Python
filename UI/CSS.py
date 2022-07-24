import sys
# from PySide6 import QtWidgets
from PySide2 import QtWidgets
# from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

# create the application and the main window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

# setup stylesheet
apply_stylesheet(app, theme='dark_teal.xml') # 颜色 theme=['dark_amber.xml','dark_blue.xml','dark_cyan.xml','dark_lightgreen.xml',
# 'dark_pink.xml','dark_purple.xml','dark_red.xml','dark_teal.xml','dark_yellow.xml','light_amber.xml','light_blue.xml',
# 'light_cyan.xml','light_cyan_500.xml','light_lightgreen.xml','light_pink.xml','light_purple.xml','light_red.xml',
# 'light_teal.xml','light_yellow.xml'] # invert_secondary=True 浅色模式

# run
window.show()
app.exec_()