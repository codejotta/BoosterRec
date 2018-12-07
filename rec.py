from pynput import keyboard
from tkinter import *
from tkinter import filedialog
import datetime
import PIL.ImageGrab
from PIL import ImageTk

class Window:
	def __init__(self):
		self.image = None
		self.window = Tk()

		capturar = Button(self.window, text="Capturar tela", relief="ridge", bd=1, bg="#f2f3ed", command=self.capture)
		capturar.pack(side="bottom", pady=5)

		self.lb_image = Label(self.window, image=None)
		self.lb_image.pack(side="bottom")

		save_lb = Label(self.window, text="Salvar imagem:", bg="#f2f3ed")
		save_lb.pack(side="top", anchor="nw", padx=4)

		self.save_en = Entry(self.window, relief="ridge", bd=1, bg="#fff")
		self.save_en.pack(side=LEFT, ipady=3, padx=5, ipadx=100, pady=5)

		save_bt = Button(self.window, text="Salvar", relief="ridge", bd=1, bg="#f2f3ed", command=self.open_dir)
		save_bt.pack(side="left", padx=5)

		self.window.configure(padx=5, pady=8, bg="#f2f3ed")
		self.window.title("Screenshot")
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
			if folder_selected != "":
				self.save_en.insert("end", folder_selected)
				self.image.save(folder_selected)

	def capture(self):
		self.image = PIL.ImageGrab.grab()
		proportion = self.image.size[0] - self.image.size[1]
		perc = (proportion*100)/self.image.size[0]
		x = 370
		y = int(x-((x/100)*perc))
		self.im = self.image.resize((x,y), PIL.Image.ANTIALIAS)
		self.im = PIL.ImageTk.PhotoImage(image=self.im)
		self.lb_image.configure(image=self.im)


krelease = [None]

def on_release(key):
	global krelease
	key = str(key)
	key = key.strip("\'")
	krelease.append(key)
	if (krelease[-1] == "Key.ctrl_l" and krelease[-2] == "m") or (krelease[-1] == "m" and krelease[-2] == "Key.ctrl_l"): # CTRL + M
		Window() # CTRL + M

if __name__ == "__main__":
	with keyboard.Listener(on_release=on_release) as listener:
		listener.join()