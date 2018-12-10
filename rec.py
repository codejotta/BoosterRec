import sys
from PySide2.QtWidgets import (QApplication, QMessageBox, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QGroupBox, 
								QSystemTrayIcon, QMenu, QCheckBox, QAction, QShortcut, QRubberBand, QDialog)
from PySide2.QtGui import QIcon, QPixmap, QImage, QKeySequence, QCursor, QPalette, QBrush
from PySide2.QtCore import Qt, QCoreApplication, QThread, QTimer, QObject, SIGNAL, QRect, QSize, QPoint
from pynput import keyboard
from _thread import start_new_thread

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.initUI()

	def initUI(self):
		folderLabel = QLabel("Pasta:")
		folderLabel.setFixedWidth(30)
		self.folderEntry = QLineEdit(sys.path[0]+"\\"+"screenshot.png", self)
		self.folderEntry.setFixedWidth(300)
		folderButton = QPushButton("Procurar...", self)
		folderButton.setFixedWidth(75)
		folderButton.clicked.connect(self.open_folder)
		folderLayout = QHBoxLayout()
		folderLayout.addWidget(folderLabel)
		folderLayout.addWidget(self.folderEntry)
		folderLayout.addWidget(folderButton)

		boxImage = QGroupBox("Captura da tela")
		boxLayout = QVBoxLayout()
		self.screenFrame = QLabel("Tela não capturada.", boxImage)
		boxLayout.addWidget(self.screenFrame)
		boxImage.setLayout(boxLayout)

		optionsGroup = QGroupBox("Opções")
		screen_width = QApplication.primaryScreen().grabWindow(0).size().width()
		screen_height = QApplication.primaryScreen().grabWindow(0).size().height()
		self.area_total = QCheckBox("Capturar a tela inteira (%sx%s)"%(screen_width, screen_height), checked=1)
		self.area_total.clicked.connect(self.total_area_function)
		self.specific_area = QCheckBox("Capturar área específica", checked=0)
		self.specific_area.clicked.connect(self.specific_area_function)
		self.no_capture_window = QCheckBox("Não capturar esta janela")
		optionsLayout = QVBoxLayout()
		optionsLayout.addWidget(self.area_total)
		optionsLayout.addWidget(self.specific_area)
		optionsLayout.addWidget(self.no_capture_window)
		optionsGroup.setLayout(optionsLayout)

		captureButton = QPushButton("Capturar tela", self)
		captureButton.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_C))
		captureButton.setFixedWidth(85)
		captureButton.clicked.connect(self.capture)
		optionsButton = QPushButton("Ocultar", self)
		optionsButton.setShortcut(QKeySequence(Qt.Key_Escape))
		optionsButton.setFixedWidth(85)
		optionsButton.clicked.connect(self.hidden_window_main)
		saveButton = QPushButton("Salvar Imagem", self)
		saveButton.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
		saveButton.setFixedWidth(85)
		saveButton.clicked.connect(self.save_image)
		bottomLayout = QGridLayout()
		bottomLayout.addWidget(captureButton,0,0)
		bottomLayout.addWidget(optionsButton,0,1)
		bottomLayout.addWidget(QLabel(),0,2)
		bottomLayout.addWidget(saveButton,0,3)

		self.layout = QVBoxLayout()
		self.layout.addLayout(folderLayout)
		self.layout.addWidget(boxImage)
		self.layout.addWidget(optionsGroup)
		self.layout.addLayout(bottomLayout)
		self.layout.setAlignment(Qt.AlignLeft)
		self.layout.setAlignment(Qt.AlignTop)

		self.setLayout(self.layout)
		self.setMaximumWidth(0)
		self.setMaximumHeight(0)
		self.setWindowTitle('Booster Rec')
		self.setWindowIcon(QIcon('icon.png'))

	def specific_area_function(self):
		if self.specific_area.isChecked() == True:
			self.area_total.setChecked(False)

	def total_area_function(self):
		if self.area_total.isChecked() == True:
			self.specific_area.setChecked(False)

	def open_folder(self):
		folder = QFileDialog.getSaveFileName(self, 'Selecionar pasta', '', "PNG (*.png);;JPEG (*.jpg);; Todos arquivos (*.*)")
		if folder[0] != "":
			self.folderEntry.setText(folder[0])

	def hidden_window_main(self):
		self.setVisible(False)

	def save_image(self):
		folder = self.folderEntry.text()
		self.image.save(folder)
		msg_info = QMessageBox(self)
		msg_info.setIcon(QMessageBox.Information)
		msg_info.setWindowTitle("Info")
		msg_info.setText("Imagem salva!")
		msg_info.setStandardButtons(QMessageBox.Ok)
		self.layout.addWidget(msg_info)

	def closeEvent(self, event):
		self.hide()
		event.ignore()
		trayIcon.setVisible(True)

	def capture(self):
		if self.no_capture_window.isChecked() == True:
			self.setVisible(False)
			QThread.msleep(210)
		self.image = QApplication.primaryScreen().grabWindow(0)
		self.setVisible(True)

		if self.area_total.isChecked() == True:
			width = 400
			height = width
			self.screenFrame.setPixmap(self.image.scaled(width,height,Qt.KeepAspectRatio, Qt.SmoothTransformation))
		elif self.specific_area.isChecked() == True:
			img = self.image
			FullScreenImage(img)


class FullScreenImage(QDialog):
	def __init__(self, image, parent=None):
		super(FullScreenImage, self).__init__(parent)

		self.image = image
		self.img = QLabel(self)
		self.img.setPixmap(self.image)

		colorRubber = QPalette()
		colorRubber.setBrush(QPalette.Highlight, Qt.transparent)
		transparent = QRubberBand(QRubberBand.Rectangle, self)
		transparent.setGeometry(QRect(QPoint(0,0), QSize(self.image.size().width(),self.image.size().height())))
		transparent.setPalette(colorRubber)
		transparent.show()

		self.setCursor(Qt.CrossCursor)
		self.setWindowState(Qt.WindowFullScreen)
		self.exec_()
	def mousePressEvent(self, event):
		self.origin_cursor = event.pos()
		self.currentQRubberBand = QLabel(self)
		self.currentQRubberBand.setGeometry(QRect(self.origin_cursor, QSize()))
		self.currentQRubberBand.show()
	def mouseMoveEvent(self, event):
		self.currentQRubberBand.setGeometry(QRect(self.origin_cursor, event.pos()).normalized())
		self.currentQRubberBand.setPixmap(self.image.copy(self.currentQRubberBand.geometry()))
	def mouseReleaseEvent(self, event):
		self.currentQRubberBand.hide()
		currentQRect = self.currentQRubberBand.geometry()
		self.currentQRubberBand.deleteLater()
		image_final = self.image.copy(currentQRect)
		win.image = image_final
		win.screenFrame.setPixmap(image_final.scaled(400,400,Qt.KeepAspectRatio,Qt.SmoothTransformation))
		self.hide()

class SystemTrayIcon(QSystemTrayIcon):
	def __init__(self, icon, parent=None):
		QSystemTrayIcon.__init__(self, icon, parent)
		menu = QMenu(parent)
		initAction = QAction(QIcon("icon.png"), "&Mostrar/Esconder", self)
		initAction.triggered.connect(self.initUI)
		printScreen = QAction(QIcon("icon.png"), "&Capturar tela", self)
		printScreen.triggered.connect(self.capture)
		exitAction = QAction(QIcon("icon.png"), "&Exit", self)
		exitAction.triggered.connect(QCoreApplication.exit)
		menu.addAction(initAction)
		menu.addAction(printScreen)
		menu.addAction(exitAction)
		self.setContextMenu(menu)
		self.show()
	def initUI(self):
		if win.isVisible() == False:
			win.setVisible(True)
		else:
			win.setVisible(False)
	def capture(self):
		win.capture()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	trayIcon = SystemTrayIcon(QIcon("icon.png"))
	win = Window()
	sys.exit(app.exec_())