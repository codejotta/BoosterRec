import sys, time
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox
from PySide2.QtGui import QIcon

#window = QWidget()
#window.resize(250, 150)
#window.setWindowTitle('Booster Rec')
#window.show()

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.initUI()

	def initUI(self):
		#groupBox = QGroupBox("Screenshot")
		#groupBox.setLayout(layout)
		#windowLayout = QVBoxLayout()
		#windowLayout.addWidget(groupBox)

		entry = QLineEdit(self) #diretorio para salvar
		btn_save = QPushButton("Salvar", self) #button salvar
		btn_save.clicked.connect(self.save_image)

		layoutSave = QHBoxLayout()
		layoutSave.addWidget(entry)
		layoutSave.addWidget(btn_save)

		btn_capture = QPushButton("Capturar tela", self) #button capturar
		btn_capture.clicked.connect(self.capture)

		self.layout = QVBoxLayout()
		self.layout.addLayout(layoutSave)
		self.layout.addWidget(btn_capture)
		self.setLayout(self.layout)

		self.setWindowTitle('Booster Rec')
		self.setWindowIcon(QIcon('icon.png'))
		self.show()

	def save_image(self):
		print("salvar")
		msg_info = QMessageBox(self)
		msg_info.setIcon(QMessageBox.Information)
		msg_info.setWindowTitle("Info")
		msg_info.setText("Imagem salva!")
		msg_info.setStandardButtons(QMessageBox.Ok)
		self.layout.addWidget(msg_info)

	def capture(self):
		print("capturar tela")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	wi = Window()
	sys.exit(app.exec_())
