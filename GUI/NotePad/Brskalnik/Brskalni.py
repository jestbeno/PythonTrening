from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os, sys

UserInterfaceFile = "NotaBee.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType(UserInterfaceFile)

sys._excepthook = sys.excepthook

class MainWindow(QtWidgets.QMainWindow, UI_MainWindow):

	def __init__(self):
		super().__init__()

		self.setupUi(self)
		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl("http://google.com"))

		self.show()

# LOVLJENJE NAPAK!!!!
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

def main():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    # window.setWindowIcon(QtGui.QIcon('Resource/Icons/icon.png'))
    window.setWindowTitle("NotaBeeNe 1.0")
    window.showMaximized()

    # app.exec()
    # LOVLJENJE NAPAK!!!
    sys.excepthook = my_exception_hook
    try:
	    sys.exit(app.exec_())
    except:
	    print("Exiting")

if "__main__" == __name__:
    main()
