import sys
from PySide2.QtWidgets import (QApplication, QMessageBox, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QGroupBox, 
								QSystemTrayIcon, QMenu, QCheckBox, QAction, QShortcut, QPlainTextEdit)
from PySide2.QtGui import QIcon, QPixmap, QImage, QKeySequence, QCursor
from PySide2.QtCore import Qt, QCoreApplication, QThread, QTimer, QObject, SIGNAL, QRect
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
		self.screenFrame = QLabel("Tela não capturada (Uma miniatura aparecerá aqui).", boxImage)
		boxLayout.addWidget(self.screenFrame)
		boxImage.setLayout(boxLayout)

		optionsGroup = QGroupBox("Opções")
		self.area_total = QCheckBox("Capturar a tela inteira (1368x766)", checked=1)
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

		if self.area_total.isChecked() == True:
			width = 400
			height = width
			self.screenFrame.setPixmap(self.image.scaled(width,height,Qt.KeepAspectRatio, Qt.SmoothTransformation))
			self.setVisible(True)
		elif self.specific_area.isChecked() == True:
			#self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
			#self.setAttribute(Qt.WA_NoSystemBackground, True)
			#self.setAttribute(Qt.WA_TranslucentBackground, True) #fundo trasparente e aberto
			self.setVisible(True)

			values = fullsimg.img.setPixmap(self.image.scaled(1366,768,Qt.KeepAspectRatio, Qt.SmoothTransformation))
			self.image = self.image.copy(*values)

class FullScreenImage(QWidget):
	def __init__(self):
		super(FullScreenImage, self).__init__()
		#frame = QApplication.primaryScreen().grabWindow(0)
		img = QLabel(self)
		#img.setPixmap(frame.scaled(1366,768,Qt.KeepAspectRatio, Qt.SmoothTransformation))
		self.showFullScreen()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_P:
			sys.exit()
	def mousePressEvent(self, event):
		x1 = event.pos().x()
		y1 = event.pos().y()
		print(x, y)
	def mouseReleaseEvent(self, event):
		x2 = event.pos().x()
		y2 = event.pos().y()

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
	fullsimg = FullScreenImage()
	sys.exit(app.exec_())