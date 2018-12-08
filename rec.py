import sys, time
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PySide2.QtGui import QIcon, QPixmap, QImage
from PySide2.QtCore import Qt
import PIL.ImageGrab
from PIL.ImageQt import ImageQt

#window = QWidget()
#window.resize(250, 150)
#window.setWindowTitle('Booster Rec')
#window.show()

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.initUI()

	def initUI(self):
		folderLabel = QLabel("Pasta:")
		folderLabel.setFixedWidth(30)
		folderEntry = QLineEdit("C:\\", self)
		folderEntry.setFixedWidth(300)
		folderButton = QPushButton("Procurar...", self)
		folderButton.setFixedWidth(75)
		folderButton.clicked.connect(self.open_folder)
		folderLayout = QHBoxLayout()
		folderLayout.addWidget(folderLabel)
		folderLayout.addWidget(folderEntry)
		folderLayout.addWidget(folderButton)

		self.screenFrame = QLabel(self)
		self.capture()

		captureButton = QPushButton("Capturar tela", self)
		captureButton.setFixedWidth(100)
		captureButton.clicked.connect(self.capture)
		saveButton = QPushButton("Salvar Imagem", self)
		saveButton.setFixedWidth(100)
		saveButton.clicked.connect(self.save_image)
		bottomLayout = QHBoxLayout()
		bottomLayout.addWidget(captureButton)
		bottomLayout.addWidget(saveButton)
		bottomLayout.setSpacing(218)
		bottomLayout.setAlignment(Qt.AlignCenter)

		self.layout = QVBoxLayout()
		self.layout.addLayout(folderLayout)
		self.layout.addWidget(self.screenFrame)
		self.layout.addLayout(bottomLayout)
		self.layout.setAlignment(Qt.AlignLeft)
		self.layout.setAlignment(Qt.AlignTop)
		self.setLayout(self.layout)

		self.setWindowTitle('Booster Rec')
		self.setWindowIcon(QIcon('icon.png'))
		self.show()

	def open_folder(self):
		pass

	def save_image(self):
		msg_info = QMessageBox(self)
		msg_info.setIcon(QMessageBox.Information)
		msg_info.setWindowTitle("Info")
		msg_info.setText("Imagem salva!")
		msg_info.setStandardButtons(QMessageBox.Ok)
		self.layout.addWidget(msg_info)

	def capture(self):
		self.image = PIL.ImageGrab.grab()
		self.image.save("oi.png")
		proportion = self.image.size[0] - self.image.size[1]
		perc = (proportion*100)/self.image.size[0]
		x = 415
		y = int(x-((x/100)*perc))
		img = self.image.resize((x,y), PIL.Image.ANTIALIAS)
		img = ImageQt(img)
		img = QPixmap.fromImage(img)
		self.screenFrame.setPixmap(img)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	wi = Window()
	sys.exit(app.exec_())
