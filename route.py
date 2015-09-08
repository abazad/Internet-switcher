from tkinter import *
import tkinter.messagebox
import re
import subprocess
import os

#-------------------------------------------

dummyTest=False

if dummyTest: command='type "'+os.path.dirname(os.path.realpath(__file__))+'\dummy_routes.txt"'
else: command='route print 0.0.0.0'

p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
out,err=p.communicate()
out=out.decode()

result=re.findall('[ \t]+(0.0.0.0)[ \t]+(0.0.0.0)[ \t]+([0-9.]{7,})[ \t]+([0-9.]{7,})[ \t]+([0-9]+)', out)

routes=[]
for i in range(len(result)):
	routes.append({'ip':result[i][2], 'metric':int(result[i][4]), 'last_command':''})

active=0
for i in range(len(routes)):
	if(routes[i]['metric']<routes[active]['metric']): active=i

print('=================')
print(routes)
print('=================')

#-------------------------------------------
	
class Application(Frame):

#-------------------------------------------

	def createWidgets(self):
		
		self.onColor='#0f0'
		self.offColor='#999'
		self.active=active
		
		for i in range(1, len(result)+1):
			
			btn=Button(self)
			btn.grid(row=i,column=1, sticky='we', padx=5, pady=5)
			btn["text"]=result[i-1][2]
			
			frm=Frame(self)
			frm.grid(row=i,column=2, padx=5, pady=5)
			frm['bg']='#000'
			frm.grid(row=i,column=2, padx=5, pady=5)
			frm=Frame(frm, width=18, height=18)
			if(i-1==active):
				frm['bg']=self.onColor
				routes[i-1]['stat']='on'
				#self.active=i-1
			else:
				frm['bg']=self.offColor
				routes[i-1]['stat']='off'
			routes[i-1]['led']=frm
			frm.pack({"side": "left", 'padx': 1, 'pady': 1})
			btn["command"] = lambda i=i-1: self.btnClick(i)

#-------------------------------------------
			
	def showError(self, o):
		tkinter.messagebox.showerror('Error!', o)
		root.quit()

#-------------------------------------------

	def routeCommand(self, i, kind, metric=1):
		command='route '+kind+' 0.0.0.0 mask 0.0.0.0 '+routes[i]['ip']+' metric '+str(metric)
		routes[i]['last_command']=kind
		print('=============================================================')
		print(command)
		print('-------------------------------------------------------------')
		ret=os.system(command)
		print('return code: ', ret)
		print('=============================================================')

#-------------------------------------------		
		
	def btnClick(self, i):
		
		if(routes[i]['stat']=='off'):
			if(self.active!=None):
				self.routeCommand(self.active, 'delete')
				routes[self.active]['led']['bg']=self.offColor
				routes[self.active]['stat']='off'
			self.routeCommand(i, 'add')
			routes[i]['led']['bg']=self.onColor
			routes[i]['stat']='on'
			self.active=i
		else:
			for j in range(len(routes)):
				self.routeCommand(j, 'delete')	
			routes[i]['led']['bg']=self.offColor
			routes[i]['stat']='off'
			self.active=None

#-------------------------------------------
			
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		print(routes)

#-------------------------------------------
		
root = Tk()
root.title('Default root')
app = Application(master=root)
app.mainloop()
root.destroy()
