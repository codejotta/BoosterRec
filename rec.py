import sys
from PySide2.QtWidgets import (QApplication, QMessageBox, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QGroupBox, 
								QSystemTrayIcon, QMenu, QAction)
from PySide2.QtGui import QIcon, QPixmap, QImage
from PySide2.QtCore import Qt, QCoreApplication
from PIL import ImageQt, ImageGrab, Image

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

		box = QGroupBox("Última captura da tela")
		boxLayout = QVBoxLayout()
		self.screenFrame = QLabel(box)
		self.capture()
		boxLayout.addWidget(self.screenFrame)
		box.setLayout(boxLayout)

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
		self.layout.addWidget(box)
		self.layout.addLayout(bottomLayout)
		self.layout.setAlignment(Qt.AlignLeft)
		self.layout.setAlignment(Qt.AlignTop)

		self.setLayout(self.layout)
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
		self.image = ImageGrab.grab()
		proportion = self.image.size[0] - self.image.size[1]
		perc = (proportion*100)/self.image.size[0]
		x = 415
		y = int(x-((x/100)*perc))
		img = self.image.resize((x,y), Image.ANTIALIAS)
		img = ImageQt.ImageQt(img)
		img = QPixmap.fromImage(img)
		self.screenFrame.setPixmap(img)

	def closeEvent(self, event):
		print("AD")
		self.hide()
		event.ignore()

class SystemTrayIcon(QSystemTrayIcon):
	def __init__(self, icon, parent=None):
		QSystemTrayIcon.__init__(self, icon, parent)
		menu = QMenu(parent)
		exitAction = menu.addAction("Exit")
		exitAction.triggered.connect(QCoreApplication.exit)
		initAction = menu.addAction("Setup")
		initAction.triggered.connect(self.initUI)
		self.setContextMenu(menu)

	def initUI(self):
		win.show()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	trayIcon = SystemTrayIcon(QIcon("icon.png"))
	trayIcon.show()
	win = Window()
	sys.exit(app.exec_())
