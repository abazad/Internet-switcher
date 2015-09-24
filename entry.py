from tkinter import *
import os

class Dialog(Toplevel):

	def __init__(self, parent, e, title = None):
		self.e=e
		Toplevel.__init__(self, parent)
		self.transient(parent)
		if title:
			self.title(title)
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
		Label(frm, text="Enter label for "+self.e.widget['text']+':').pack({"side": "top", 'padx': 1, 'pady': 1})
		self.txt=Entry(frm)
		self.txt.pack()
		return frm

	def buttonbox(self):
		box = Frame(self)
		w = Button(box, text="Save", width=10, command=self.save, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.save)
		self.bind("<Escape>", self.cancel)
		box.pack()

	def save(self, event=None):
		self.withdraw()
		self.update_idletasks()
		self.apply(self.txt.get())
		self.cancel()

	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	def apply(self, val):
		print(val)
		