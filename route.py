from tkinter import *
import tkinter.messagebox
import re
import subprocess
import os
from async import *
import funcs

#-------------------------------------------

dummyTest=True

#-------------------------------------------

funcs.dummyTest=dummyTest

routes=funcs.queryRoutes()

minMetric=999999
for i in range(len(routes)):
	if(routes[i]['metric']<minMetric): minMetric=routes[i]['metric']

tmp=0
for i in range(len(routes)):
	if(routes[i]['metric']==minMetric): tmp+=1
if(tmp>1): undetFlag=True
else: undetFlag=False

class Application(Frame):

#-------------------------------------------

	def createWidgets(self):
		
		self.onColor='#0f0'
		self.offColor='#999'
		self.undetColor='#00f'
		
		self.undetFlag=undetFlag
		self.minMetric=minMetric
		
		for i in range(len(routes)):
			
			cur_row=i+1
			cur_route=routes[i]
			
			btn=Button(self)
			btn.grid(row=cur_row,column=1, sticky='we', padx=5, pady=5)
			btn["text"]=routes[i]['gateway']
			
			frm=Frame(self)
			frm.grid(row=cur_row,column=2, padx=5, pady=5)
			frm['bg']='#000'
			frm.grid(row=cur_row,column=2, padx=5, pady=5)
			frm=Frame(frm, width=18, height=18)
			if(cur_route['metric2']==self.minMetric):
				if(undetFlag):
					frm['bg']=self.undetColor
					cur_route['stat']='undet'
				else:
					frm['bg']=self.onColor
					cur_route['stat']='on'
			else:
				frm['bg']=self.offColor
				cur_route['stat']='off'
			cur_route['led']=frm
			frm.pack({"side": "left", 'padx': 1, 'pady': 1})
			btn["command"] = lambda i=i: self.btnClick(i)

#-------------------------------------------

	def routeCommand(self, i, kind, metric=1):
		command='route '+kind+' 0.0.0.0 mask 0.0.0.0 '+routes[i]['gateway']+' metric '+str(metric)
		print('=============================================================')
		print(command)
		if(not dummyTest): os.system(command)
		print('=============================================================')
		routes[i]['metric2']=metric

#-------------------------------------------		

	def delAllRoutes(self):
		for i in range(len(routes)):
			if(routes[i]['stat']!='del'):
				self.routeCommand(i, 'delete')
				routes[i]['stat']='del'
				routes[i]['led']['bg']=self.offColor		

#-------------------------------------------		

	def routeOn(self, i):
		self.routeCommand(i, 'add')
		routes[i]['led']['bg']=self.onColor
		routes[i]['stat']='on'

#-------------------------------------------		

	def routeOff(self, i):
		if(routes[i]['stat']!='del'):
			if(routes[i]['metric2']<=1):
				self.routeCommand(i, 'add', 2)
			routes[i]['stat']='off'
			routes[i]['led']['bg']=self.offColor

#-------------------------------------------		
		
	def btnClick(self, i):
		if(routes[i]['stat']!='on'):
			for j in range(len(routes)): self.routeOff(j)
			self.routeOn(i)
		else:
			self.delAllRoutes()

#-------------------------------------------
	def test(self):
		print('test...\n')
#-------------------------------------------
			
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		print('====================================================================')
		print(routes)
		print('====================================================================')

#-------------------------------------------
		
root=Tk()
root.title('Internet switcher')
app=Application(master=root)
app.routes=routes
async=Async(app)
#async.mainApp=app
async.start()
app.mainloop()
