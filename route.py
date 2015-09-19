from tkinter import *
import re
import subprocess
import os
import sys

#-------------------------------------------

dummyTest=False

routesCheckInterval=3 #in seconds

#-------------------------------------------

class Application(Frame):

#-------------------------------------------
	
	def queryRoutes(self):
	
		if dummyTest: command='type "'+os.path.dirname(os.path.realpath(__file__))+'\dummy_routes.txt"'
		else: command='route print 0.0.0.0'

		p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out,err=p.communicate()
		out=out.decode()

		result=re.findall('[ \t]+(0.0.0.0)[ \t]+(0.0.0.0)[ \t]+([0-9.]{7,})[ \t]+([0-9.]{7,})[ \t]+([0-9]+)', out)

		routes=[]
		for i in range(len(result)):
			routes.append({'gateway':result[i][2], 'metric':int(result[i][4]), 'metric2': int(result[i][4])})
			
		result=re.findall('[ \t]*Default Gateway:[ \t]+([0-9.]{7,})', out)
		if(len(result)): self.defaultGateway=result[0]
		else: self.defaultGateway=''
		
		return routes

#-------------------------------------------
		
	def createWidgets(self):
		
		self.onColor='#0f0'
		self.offColor='#999'
		
		self.routes=self.queryRoutes()
		
		self.container=container=Frame(self)
		container.pack()
		
		for i in range(len(self.routes)):
			
			cur_row=i+1
			cur_route=self.routes[i]
			
			btn=Button(container)
			btn.grid(row=cur_row,column=1, sticky='we', padx=5, pady=5)
			btn["text"]=self.routes[i]['gateway']
			
			frm=Frame(container)
			frm.grid(row=cur_row,column=2, padx=5, pady=5)
			frm['bg']='#000'
			frm=Frame(frm, width=18, height=18)
			if(cur_route['gateway']==self.defaultGateway):
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
		command='route '+kind+' 0.0.0.0 mask 0.0.0.0 '+self.routes[i]['gateway']+' metric '+str(metric)
		print('=============================================================')
		print(command)
		if(not dummyTest):
			p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out,err=p.communicate()
			if(err):
				if(sys.stdin):
					err=err.decode()
					print('---------------------------------------------')
					print(err)
		print('=============================================================')
		self.routes[i]['metric2']=metric

#-------------------------------------------		

	def delAllRoutes(self):
		for i in range(len(self.routes)):
			if(self.routes[i]['stat']!='del'):
				self.routeCommand(i, 'delete')
				self.routes[i]['stat']='del'
				self.routes[i]['led']['bg']=self.offColor		

#-------------------------------------------		

	def routeOn(self, i):
		self.routeCommand(i, 'add')
		self.routes[i]['led']['bg']=self.onColor
		self.routes[i]['stat']='on'

#-------------------------------------------		

	def routeOff(self, i):
		if(self.routes[i]['stat']!='del'):
			if(self.routes[i]['metric2']<=1):
				self.routeCommand(i, 'add', 2)
			self.routes[i]['stat']='off'
			self.routes[i]['led']['bg']=self.offColor

#-------------------------------------------		
		
	def btnClick(self, i):
		if(self.routes[i]['stat']!='on'):
			for j in range(len(self.routes)): self.routeOff(j)
			self.routeOn(i)
		else:
			self.delAllRoutes()

#-------------------------------------------

	def check(self):
		return
		routes1=self.routes
		routes2=self.queryRoutes()
		changed=False
		if(len(routes1) and routes1[0]['stat']=='del'):
			if(len(routes2)): changed=True
		elif(len(routes2)!=len(routes1)): changed=True
		else:
			for i in range(len(routes2)):
				if(routes2[i]['gateway']!=routes1[i]['gateway']):
					changed=True
					break
		if(changed):
			print('route changes detected')
			self.container.destroy()
			self.createWidgets()
		self.after(routesCheckInterval*1000, self.check)

#-------------------------------------------
			
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		print('====================================================================')
		print(self.routes)
		print('====================================================================')
		self.after(routesCheckInterval*1000, self.check)

#-------------------------------------------
		
root=Tk()
root.title('Internet switcher')
app=Application(master=root)
app.mainloop()
