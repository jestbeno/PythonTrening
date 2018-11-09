# App used for learning process - (almost) all credits goes to:
# https://martinfitzpatrick.name/
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import Qt

from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtWidgets import qApp, QMessageBox,QAction,QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,QFontComboBox, QComboBox,QActionGroup
# from PyQt5.QtGui import QIcon,QPixmap,QFont,QKeySequence

# from PyQt5.QtPrintSupport import QPrintDialog
import os.path
import os,sys
import shutil
from PIL import Image

import operator

import openpyxl
from lxml import etree

UserInterfaceFile = "NotePad.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType(UserInterfaceFile)

sys._excepthook = sys.excepthook

# print (help(QtCore.Qt))

# Calculator state.
READY = 0
INPUT = 1

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
HTML_EXTENSIONS = ['.htm', '.html']

class MainWindow(QtWidgets.QMainWindow, UI_MainWindow):

	def __init__(self):
		super().__init__()

		# self.setWindowTitle("BeeEditor")
		self.setupUi(self)

		self.textEdit.selectionChanged.connect(self.update_format)

		# Initialize default font size.
		font = QFont('Times', 12)
		self.textEdit.setFont(font)
		# We need to repeat the size to init the current format.
		self.textEdit.setFontPointSize(12)

		self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.textEdit.showMaximized()
		print(help(self.textEdit))
		self.ToolBar()

		self.actionIzhod.triggered.connect(self.ZapriApp)
		self.path = None

		# A list of all format-related widgets/actions, so we can disable/enable signals when updating.
		self._format_actions = [
			self.fonts,
			self.fontsize,
			self.bold_action,
			self.italic_action,
			self.underline_action,
			# We don't need to disable signals for alignment, as they are paragraph-wide.
		]

		# Initialize.
		self.update_format()
		self.update_title()
		self.show()

	def block_signals(self, objects, b):
		for o in objects:
			o.blockSignals(b)

	def update_format(self):
		"""
		Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
		toolbars/etc. in sync with the current edit state.
		:return:
		"""
		# Disable signals for all format widgets, so changing values here does not trigger further formatting.
		self.block_signals(self._format_actions, True)

		self.fonts.setCurrentFont(self.textEdit.currentFont())
		# Nasty, but we get the font-size as a float but want it was an int
		self.fontsize.setCurrentText(str(int(self.textEdit.fontPointSize())))

		self.italic_action.setChecked(self.textEdit.fontItalic())
		self.underline_action.setChecked(self.textEdit.fontUnderline())
		self.bold_action.setChecked(self.textEdit.fontWeight() == QFont.Bold)

		self.alignl_action.setChecked(self.textEdit.alignment() == Qt.AlignLeft)
		self.alignc_action.setChecked(self.textEdit.alignment() == Qt.AlignCenter)
		self.alignr_action.setChecked(self.textEdit.alignment() == Qt.AlignRight)
		self.alignj_action.setChecked(self.textEdit.alignment() == Qt.AlignJustify)

		self.block_signals(self._format_actions, False)


	def dialog_critical(self, s):
		dlg = QMessageBox(self)
		dlg.setText(s)
		dlg.setIcon(QMessageBox.Critical)
		dlg.show()

	def file_open(self):
		path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
		                                      "HTML(*.html);Text(*.txt);All files (*.*)")

		try:
			with open(path, 'r') as f:
				text = f.read()

		except Exception as e:
			self.dialog_critical(str(e))

		else:
			self.path = path
			# Qt will automatically try and guess the format as txt/html
			self.textEdit.setText(text)
			self.update_title()

	def file_save(self):
		if self.path is None:
			# If we do not have a path, we need to use Save As.
			return self.file_saveas()

		text = self.textEdit.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.textEdit.toPlainText()

		try:
			with open(self.path, 'w') as f:
				f.write(text)

		except Exception as e:
			self.dialog_critical(str(e))

	def file_saveas(self):
		path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
		                                      "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

		if not path:
			# If dialog is cancelled, will return ''
			return

		text = self.textEdit.toHtml() if splitext(path) in HTML_EXTENSIONS else self.textEdit.toPlainText()

		try:
			with open(path, 'w') as f:
				f.write(text)

		except Exception as e:
			self.dialog_critical(str(e))

		else:
			self.path = path
			self.update_title()

	def file_print(self):
		dlg = QPrintDialog()
		if dlg.exec_():
			self.textEdit.print_(dlg.printer())

	def ToolBar(self):
		toolbar = self.addToolBar('Toolbar')
		self.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)

		openAction = QAction(QIcon('images/blue-folder-open-document.png'), 'Open (Ctrl+O)', self)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Odpri (Ctrl+Q)')
		openAction.triggered.connect(self.file_open)
		toolbar.addAction(openAction)

		toolbar.addSeparator()

		saveAction = QAction(QIcon('images/disk.png'), 'Shrani (Ctrl+S)', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip('Shrani (Ctrl+S)')
		saveAction.triggered.connect(self.file_save)
		toolbar.addAction(saveAction)

		saveAsAction = QAction(QIcon('images/disk--pencil.png'), 'Shrani (Ctrl+S)', self)
		saveAsAction.setShortcut('Ctrl+S')
		saveAsAction.setStatusTip('Shrani (Ctrl+S)')
		saveAsAction.triggered.connect(self.file_saveas)
		toolbar.addAction(saveAsAction)

		copyAction = QAction(QIcon('images/document-copy.png'), 'Kopiraj (Ctrl+C)', self)
		copyAction.setShortcut('Ctrl+C')
		copyAction.setStatusTip('Kopiraj (Ctrl+C)')
		copyAction.triggered.connect(self.ZapriApp)
		toolbar.addAction(copyAction)

#############################################################

		format_toolbar = self.addToolBar('Format')
		self.addToolBar(QtCore.Qt.TopToolBarArea, format_toolbar)
		# format_toolbar = QToolBar("Format")
		# format_toolbar.setIconSize(QSize(16, 16))
		# self.addToolBar(format_toolbar)

		# TO LAHKO UREDIŠ V DESIGNERJU!!!
		format_menu = self.menuBar().addMenu("&Format")

		# We need references to these actions/settings to update as selection changes, so attach to self.
		self.fonts = QFontComboBox()
		self.fonts.currentFontChanged.connect(self.textEdit.setCurrentFont)
		format_toolbar.addWidget(self.fonts)

		self.fontsize = QComboBox()
		self.fontsize.addItems([str(s) for s in FONT_SIZES])

		# Connect to the signal producing the text of the current selection. Convert the string to float
		# and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
		self.fontsize.currentIndexChanged[str].connect(lambda s: self.textEdit.setFontPointSize(float(s)))
		format_toolbar.addWidget(self.fontsize)

		self.bold_action = QAction(QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)
		self.bold_action.setStatusTip("Bold")
		self.bold_action.setShortcut(QKeySequence.Bold)
		self.bold_action.setCheckable(True)
		self.bold_action.toggled.connect(lambda x: self.textEdit.setFontWeight(QFont.Bold if x else QFont.Normal))
		format_toolbar.addAction(self.bold_action)
		format_menu.addAction(self.bold_action)

		self.italic_action = QAction(QIcon(os.path.join('images', 'edit-italic.png')), "Italic", self)
		self.italic_action.setStatusTip("Italic")
		self.italic_action.setShortcut(QKeySequence.Italic)
		self.italic_action.setCheckable(True)
		self.italic_action.toggled.connect(self.textEdit.setFontItalic)
		format_toolbar.addAction(self.italic_action)
		format_menu.addAction(self.italic_action)

		self.underline_action = QAction(QIcon(os.path.join('images', 'edit-underline.png')), "Underline", self)
		self.underline_action.setStatusTip("Underline")
		self.underline_action.setShortcut(QKeySequence.Underline)
		self.underline_action.setCheckable(True)
		self.underline_action.toggled.connect(self.textEdit.setFontUnderline)
		format_toolbar.addAction(self.underline_action)
		format_menu.addAction(self.underline_action)

		format_menu.addSeparator()

		self.alignl_action = QAction(QIcon(os.path.join('images', 'edit-alignment.png')), "Align left", self)
		self.alignl_action.setStatusTip("Align text left")
		self.alignl_action.setCheckable(True)
		self.alignl_action.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignLeft))
		format_toolbar.addAction(self.alignl_action)
		format_menu.addAction(self.alignl_action)

		self.alignc_action = QAction(QIcon(os.path.join('images', 'edit-alignment-center.png')), "Align center", self)
		self.alignc_action.setStatusTip("Align text center")
		self.alignc_action.setCheckable(True)
		self.alignc_action.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignCenter))
		format_toolbar.addAction(self.alignc_action)
		format_menu.addAction(self.alignc_action)

		self.alignr_action = QAction(QIcon(os.path.join('images', 'edit-alignment-right.png')), "Align right", self)
		self.alignr_action.setStatusTip("Align text right")
		self.alignr_action.setCheckable(True)
		self.alignr_action.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignRight))
		format_toolbar.addAction(self.alignr_action)
		format_menu.addAction(self.alignr_action)

		self.alignj_action = QAction(QIcon(os.path.join('images', 'edit-alignment-justify.png')), "Justify", self)
		self.alignj_action.setStatusTip("Justify text")
		self.alignj_action.setCheckable(True)
		self.alignj_action.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignJustify))
		format_toolbar.addAction(self.alignj_action)
		format_menu.addAction(self.alignj_action)

		format_group = QActionGroup(self)
		format_group.setExclusive(True)
		format_group.addAction(self.alignl_action)
		format_group.addAction(self.alignc_action)
		format_group.addAction(self.alignr_action)
		format_group.addAction(self.alignj_action)

		format_menu.addSeparator()

		printAction = QAction(QIcon('images/printer.png'), 'Natisni (Ctrl+P)', self)
		printAction.setShortcut('Ctrl+P')
		printAction.setStatusTip('Natisni (Ctrl+P)')
		printAction.triggered.connect(self.file_print)
		toolbar.addAction(printAction)

		# exitAction = QAction(QIcon('images/Izhod.png'), 'Izhod (Ctrl+Q)', self)
		# exitAction.setShortcut('Ctrl+Q')
		# exitAction.setStatusTip('Izhod (Ctrl+Q)')
		# exitAction.triggered.connect(self.ZapriApp)
		# toolbar.addAction(exitAction)

	def update_title(self):
		updated_title = os.path.basename(self.path) if self.path else "Neimenovan"
		self.setWindowTitle(f"{updated_title} - ToBee editor" )

	def edit_toggle_wrap(self):
		self.textEdit.setLineWrapMode(1 if self.textEdit.lineWrapMode() == 0 else 0)

	''' ---------------------------------------------
	Zapri aplikacijo
	----------------------------------------------'''

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


def splitext(p):
	a = os.path.splitext(p)[1].lower()
	print (a)
	return a


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

