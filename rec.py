from pynput import keyboard
import pyscreenshot as get_screen
from tkinter import *
from tkinter import filedialog
import datetime

krelease = [None]

class Window:
	def __init__(self, image):
		self.image = image
		self.window = Tk()

		save_lb = Label(self.window, text="Salvar arquivo:", bg="#f2f3ed")
		save_lb.pack(side="top", anchor="nw", padx=4)

		self.save_en = Entry(self.window, relief="ridge", bd=1, bg="#fff")
		self.save_en.pack(side=LEFT, ipady=3, padx=5, ipadx=100)

		save_bt = Button(self.window, text="Salvar", relief="ridge", bd=1, bg="#f2f3ed", command=self.open_dir)
		save_bt.pack(side="left", padx=5)

		self.window.configure(padx=5, pady=8, bg="#f2f3ed")
		self.window.title("Salvar screenshot")
		self.window.mainloop()

	def open_dir(self):
		options = {}
		options['defaultextension'] = ".png"
		options['filetypes'] = [('PNG (*.png)', '.png'),('All Files (*.*)', '.*')]
		options['initialfile'] = str(datetime.datetime.now())[:10]
		options['title'] = "Salvar screenshot - Escolher Diretorio"

		if self.save_en.get() != "":
			folder = self.save_en.get()
			try:
				self.image.save(folder)
			except ValueError:
				folder = folder + ".png"
				self.image.save(folder)
				self.save_en.delete(0,"end")
				self.save_en.insert(0, folder)
		else:
			folder_selected = filedialog.asksaveasfilename(**options)
			self.save_en.insert("end", folder_selected)
			self.image.save(folder_selected)

def on_release(key):
	global krelease
	key = str(key)
	key = key.strip("\'")
	krelease.append(key)
	if (krelease[-1] == "Key.ctrl_l" and krelease[-2] == "m") or (krelease[-1] == "m" and krelease[-2] == "Key.ctrl_l"):
		image = get_screen.grab()
		Window(image)
	print(krelease)

if __name__ == "__main__":
	with keyboard.Listener(on_release=on_release) as listener:
		listener.join()