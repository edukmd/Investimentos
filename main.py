from backend import GetData
from frontend import MyWidget
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

url = 'https://www.fundsexplorer.com.br/ranking'

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = MyWidget()


    sys.exit(app.exec_())
