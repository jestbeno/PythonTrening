from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QListWidget,QTextEdit
from PyQt5.QtCore import Qt
import sys

UserInterfaceFile = "Dockable.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType(UserInterfaceFile)

# Calculator state.
READY = 0
INPUT = 1

class Calculator(QtWidgets.QMainWindow, UI_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		UI_MainWindow.__init__(self)

		self.setupUi(self)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "DockAble Application"
        top = 400
        left = 400
        width = 600
        height = 500

        icon = "icon.png"

        self.setWindowTitle(title)
        self.setGeometry(top,left, width, height)
        self.setWindowIcon(QIcon("icon.png"))

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.dockAble()

        self.show()

    def dockAble(self):
        dock = QDockWidget("Fruits", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.myfruit = ["App", "Melon", "Pear", "Banana"]
        self.listwidget = QListWidget(dock)
        self.listwidget.addItems(self.myfruit)
        dock.setWidget(self.listwidget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        dock = QDockWidget("Employee", self)
        self.employee = ["John", "Doe", "Parwiz", "Bob"]
        self.listwidget2 = QListWidget(dock)
        self.listwidget2.addItems(self.employee)
        dock.setWidget(self.listwidget2)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()

# App used for learning process - (almost) all credits goes to:
# https://martinfitzpatrick.name/

from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from PyQt5.QtWidgets import qApp, QMessageBox,QAction
from PyQt5.QtGui import QIcon,QPixmap
import os.path
import os,sys
import shutil
from PIL import Image

import operator

import openpyxl
import os
from lxml import etree


UserInterfaceFile = "Calculator.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType(UserInterfaceFile)

# Calculator state.
READY = 0
INPUT = 1

class Calculator(QtWidgets.QMainWindow, UI_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		UI_MainWindow.__init__(self)

		self.setupUi(self)

		# get number and display it!
		for n in range(0, 10):
			getattr(self, 'pushButton_n%s' % n).pressed.connect(lambda v=n: self.input_number(v))

		self.pushButton_add.pressed.connect(lambda: self.operation(operator.add))
		self.pushButton_sub.pressed.connect(lambda: self.operation(operator.sub))
		self.pushButton_mul.pressed.connect(lambda: self.operation(operator.mul))
		self.pushButton_div.pressed.connect(lambda: self.operation(operator.truediv))

		self.pushButton_pc.pressed.connect(self.operation_pc)

		# self.pushButton_eq.setShortcut("")
		self.pushButton_eq.pressed.connect(self.equals)

# reseting values
		self.actionReset.triggered.connect(self.reset)
		self.pushButton_ac.pressed.connect(self.reset)

		self.pushButton_m.pressed.connect(self.memory_store)
		self.pushButton_mr.pressed.connect(self.memory_recall)

		self.memory = 0
		self.reset()

		self.show()

	def display(self):
		self.lcdNumber.display(self.stack[-1])

		# print (str(self.stack[0])+ " - stack 0")
		# print (str(self.stack[-1])+ " - stack -1")

	def reset(self):
		self.state = READY
		self.stack = [0]
		self.last_operation = None
		self.current_op = None
		self.display()

	def memory_store(self):
		self.memory = self.lcdNumber.value()

	def memory_recall(self):
		# self.state = INPUT
		self.stack[-1] = self.memory
		self.display()

	def input_number(self, v):
		if self.state == READY:
			self.state = INPUT
			self.stack[-1] = v
		else:
			self.stack[-1] = self.stack[-1] * 10 + v
		self.display()


	def operation(self, op):
		if self.current_op:  # Complete the current operation
			self.equals()

		self.stack.append(0)
		self.state = INPUT
		self.current_op = op


	def operation_pc(self):
		self.state = INPUT
		self.stack[-1] *= 0.01
		self.display()


	def equals(self):
		# Support to allow '=' to repeat previous operation
		# if no further input has been added.
		if self.state == READY and self.last_operation:
			s, self.current_op = self.last_operation
			self.stack.append(s)

		if self.current_op:
			self.last_operation = self.stack[-1], self.current_op

			self.stack = [self.current_op(*self.stack)]
			self.current_op = None
			self.state = READY
			self.display()
def main():
    app = QtWidgets.QApplication([])
    top = Calculator()
    app.exec()

if "__main__" == __name__:
    main()

