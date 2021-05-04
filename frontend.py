import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from backend import GetData

url = 'https://www.fundsexplorer.com.br/ranking'

colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.FII = GetData(url)
        self.funds_header = self.FII.ReturnHeader()
        self.funds_list = self.FII.ReturnFundsCode()

        self.text = QtWidgets.QLabel("Lista de Fundos Imobiliários",
                                     alignment=QtCore.Qt.AlignCenter)

        self.text.setStyleSheet("background-color: yellow")
        self.text.setFont(QtGui.QFont('Arial',24))
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(len(self.funds_list))
        self.table.setColumnCount(len(self.funds_header))
        self.table.setHorizontalHeaderLabels(self.funds_header)

        self.TableWrite()
        self.table.resizeColumnsToContents()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.table)
        self.resize(800, 600)
        self.show()

    def TableWrite(self):
        for i in enumerate(self.funds_list):
            fundo = self.FII.SelectCodeInfo(i[1])
            for x in enumerate(self.funds_header):
                #print(i[0],i[1],x[0],x[1])
                print(fundo[x[1]].values[0])
                self.table.setItem(i[0], x[0], QtWidgets.QTableWidgetItem(str(fundo[x[1]].values[0])))


    def get_rgb_from_hex(code):
        code_hex = code.replace("#", "")
        rgb = tuple(int(code_hex[i:i + 2], 16) for i in (0, 2, 4))

        return QtGui.QColor.fromRgb(rgb[0], rgb[1], rgb[2])