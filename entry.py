from tkinter import *
import os
import configparser

class Dialog(Toplevel):

	def __init__(self, parent, route):
		self.route=route
		Toplevel.__init__(self, parent)
		self.transient(parent)
		self.title('Custom button label')
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)
		self.buttonbox()
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		self.wait_window(self)

	def body(self, master):
		frm=Frame(master)
		frm.pack()
		Label(frm, text="Enter label for "+self.route['btn']['text']+':').pack({"side": "top", 'padx': 1, 'pady': 1})
		self.txt=Entry(frm)
		self.txt.pack()
		return frm

	def buttonbox(self):
		box = Frame(self)
		w = Button(box, text="Save", width=10, command=self.save, default=ACTIVE)
		w.pack(padx=5, pady=5)
		Label(box, justify='left', text='Note: save an empty label to clear\n        a previously set custom label.').pack()
		self.bind("<Return>", self.save)
		self.bind("<Escape>", self.cancel)
		box.pack()


	def save(self, event=None):
		self.withdraw()
		self.update_idletasks()
		self.writeConfig(self.route['gateway'], self.txt.get())
		self.cancel()

	def cancel(self, event=None):
		self.parent.focus_set()
		self.destroy()
		
	def writeConfig(self, key, val):
		print(key+'=>'+val)
		config_file=os.path.dirname(os.path.realpath(__file__))+'\\config.ini'
		config = configparser.ConfigParser()
		config.read(config_file)
		config.set('button_labels', key, val)
		with open(config_file, 'w') as file: config.write(file)
		self.parent.container.destroy()
		self.parent.createWidgets()
		
