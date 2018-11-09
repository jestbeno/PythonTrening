from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from PyQt5.QtWidgets import qApp, QMessageBox,QAction

''' ---------------------------------------------
Zapri aplikacijo
----------------------------------------------'''

# Call from Menu bar
# self.actionIzhod.triggered.connect(self.ZapriApp)




def ZapriApp(self):
	box = QMessageBox()
	box.setIcon(QMessageBox.Question)
	box.setWindowTitle('Opozorilo')
	box.setText('Res želiš zaključiti z delom?')
	box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
	buttonY = box.button(QMessageBox.Yes)
	buttonY.setText('Da')
	buttonN = box.button(QMessageBox.No)
	buttonN.setText('Ne')
	box.exec_()
	if box.clickedButton() == buttonY:
		self.close()
	elif box.clickedButton() == buttonN:
		pass