import sys
from PySide2.QtWidgets import (QApplication, QMessageBox, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QGroupBox, 
								QSystemTrayIcon, QMenu, QCheckBox, QAction, QShortcut)
from PySide2.QtGui import QIcon, QPixmap, QImage, QKeySequence
from PySide2.QtCore import Qt, QCoreApplication, QThread, QTimer, QObject, SIGNAL
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

		boxImage = QGroupBox("Última captura da tela")
		boxLayout = QVBoxLayout()
		self.screenFrame = QLabel("Tela não capturada (Uma miniatura aparecerá aqui).", boxImage)
		boxLayout.addWidget(self.screenFrame)
		boxImage.setLayout(boxLayout)

		optionsGroup = QGroupBox("Opções")
		lb_sc = QLabel("Tecla de atalho:")
		lb_sc.setFixedWidth(80)
		self.sc_key = QLineEdit("CTRL_L+M")
		self.sc_key.setFixedWidth(50)
		ol2 = QHBoxLayout()
		ol2.addWidget(lb_sc)
		ol2.addWidget(self.sc_key)
		ol2.setAlignment(Qt.AlignTop)
		self.hidden_window = QCheckBox("Não capturar esta janela")
		optionsLayout = QVBoxLayout()
		optionsLayout.addLayout(ol2)
		optionsLayout.addWidget(self.hidden_window)
		optionsGroup.setLayout(optionsLayout)

		captureButton = QPushButton("Capturar tela", self)
		captureButton.setFixedWidth(85)
		captureButton.clicked.connect(self.capture)
		optionsButton = QPushButton("Opções", self)
		optionsButton.setFixedWidth(85)
		saveButton = QPushButton("Salvar Imagem", self)
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

	def open_folder(self):
		folder = QFileDialog.getSaveFileName(self, 'Selecionar pasta', '', "PNG (*.png);;JPEG (*.jpg);; Todos arquivos (*.*)")
		if folder[0] != "":
			self.folderEntry.setText(folder[0])

	def save_image(self):
		folder = self.folderEntry.text()
		self.image.save(folder)
		msg_info = QMessageBox(self)
		msg_info.setIcon(QMessageBox.Information)
		msg_info.setWindowTitle("Info")
		msg_info.setText("Imagem salva!")
		msg_info.setStandardButtons(QMessageBox.Ok)
		self.layout.addWidget(msg_info)

	def capture(self):
		if self.hidden_window.isChecked() == True:
			self.setVisible(False)
			QThread.msleep(210)
		self.image = QApplication.primaryScreen().grabWindow(0)
		width = 400
		height = width
		self.screenFrame.setPixmap(self.image.scaled(width,height,Qt.KeepAspectRatio, Qt.SmoothTransformation))
		self.setVisible(True)

	def closeEvent(self, event):
		self.hide()
		event.ignore()
		trayIcon.setVisible(True)

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