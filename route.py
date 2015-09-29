import tkinter.messagebox
from tkinter import *
import re
import subprocess
import os
import sys
from custom_label import *
import configparser

#-------------------------------------------

class Application(Frame):

#-------------------------------------------

	def readConfigs(self):
		global dummyTest, routesCheckInterval, onColor, offColor
		config.read(configFile)
		dummyTest=config.getboolean('main', 'dummy_test')
		routesCheckInterval=config.getint('main', 'routes_check_interval')
		onColor=config.get('main', 'on_color')
		offColor=config.get('main', 'off_color')

#-------------------------------------------

	def writeConfigs(self):
		file=open(configFile, 'w')
		config.write(file)
		file.close()

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
			routes.append({'gateway':result[i][2], 'metric':int(result[i][4]), 'metric2': int(result[i][4]), 'ip':result[i][3]})
			
		result=re.findall('[ \t]*Default Gateway:[ \t]+([0-9.]{7,})', out)
		if(len(result)): self.defaultGateway=result[0]
		else: self.defaultGateway=''
		
		return routes

#-------------------------------------------
		
	def createWidgets(self, addRoutes=None):
		
		self.readConfigs()
	
		self.routes=self.queryRoutes()
		
		if(addRoutes): self.routes=addRoutes+self.routes
		
		self.container=container=Frame(self)
		container.pack()
		
		for i in range(len(self.routes)):
			
			cur_row=i+1
			cur_route=self.routes[i]
			
			btn=Button(container)
			btn.grid(row=cur_row,column=1, sticky='we', padx=5, pady=5)
			
			cur_route['btn']=btn
			
			if(config.has_option('button_labels', cur_route['gateway']) and config.get('button_labels', cur_route['gateway'])): btn["text"]=config.get('button_labels', cur_route['gateway'])
			else: btn["text"]=cur_route['gateway']
			
			frm=Frame(container)
			frm.grid(row=cur_row,column=2, padx=5, pady=5)
			frm['bg']='#000'
			frm=Frame(frm, width=18, height=18)
			if(cur_route['gateway']==self.defaultGateway):
				frm['bg']=onColor
				cur_route['stat']='on'
			else:
				frm['bg']=offColor
				cur_route.setdefault('stat', 'off')
				#cur_route['stat']='off'
			cur_route['led']=frm
			frm.pack({"side": "left", 'padx': 1, 'pady': 1})
			btn["command"] = lambda route=cur_route: self.btnClick(route)
			btn.bind('<Button-3>', lambda event, route=cur_route: CustomLabel(self, route))

		# frm=Frame(self, height=1)
		# frm['bg']='#000'
		# frm.pack(fill='x', pady=7)
		# btn=Button(self)
		# btn["text"]='Restore all routes'
		# btn.pack(pady=5)
		# btn["command"]=self.showRoutesInfo

#-------------------------------------------

	def routeCommand(self, route, kind, metric=1):
		command='route '+kind+' 0.0.0.0 mask 0.0.0.0 '+route['gateway']+' metric '+str(metric)
		print('=============================================================')
		print(command)
		if(not dummyTest):
			p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out,err=p.communicate()
			if(err):
				err=err.decode()
				if(sys.stdout):
					print('--------------------------------------------------')
					print(err)
				else: self.showError(command+"\n\n"+err)
		print('=============================================================')
		if(not dummyTest and err): return False
		route['metric2']=metric
		return True

#-------------------------------------------

	def showError(self, e):
		tkinter.messagebox.showerror('Error!', e)
		
#-------------------------------------------

	def delAllRoutes(self):
		for route in self.routes:
			if(route['stat']!='del'):
				if(not self.routeCommand(route, 'delete')): continue
				route['stat']='del'
				route['led']['bg']=offColor		
		self.defaultGateway=''

#-------------------------------------------		

	def routeOn(self, route):
		if(not self.routeCommand(route, 'add')): return
		route['led']['bg']=onColor
		route['stat']='on'
		self.defaultGateway=route['gateway']

#-------------------------------------------		

	def routeOff(self, route):
		if(route['stat']!='del'):
			if(route['metric2']<=1):
				if(not self.routeCommand(route, 'add', 2)): return
			route['stat']='off'
			route['led']['bg']=offColor

#-------------------------------------------		
		
	def btnClick(self, route):
		if(route['stat']!='on'):
			for tmp in self.routes: self.routeOff(tmp)
			self.routeOn(route)
		else:
			self.delAllRoutes()

#-------------------------------------------

	def check(self):
		
		routes1=self.routes
		gateway1=self.defaultGateway
		
		routes2=self.queryRoutes()
		gateway2=self.defaultGateway
		
		num=0
		deletedRoutes=[]
		existentRoutes=[]
		for route in routes1:
			if(route['stat']!='del'):
				num+=1
				existentRoutes.append(route)
			else: deletedRoutes.append(route)
			
		changed=''
		if(gateway1!=gateway2): changed='default gateway changed: '+gateway1+' -> '+gateway2
		elif(len(routes2)!=num): changed='number of routes changed'
		else:
			for e in existentRoutes:
				found=False
				for  r2 in routes2:
					if(e['gateway']==r2['gateway']):
						found=True
						break
				if(not found):
					changed='some gateway changed'
					break
		
		addRoutes=[]
		if(deletedRoutes):
			ipconfig=False
			for d in deletedRoutes:
				found=False
				for r2 in routes2:
					if(d['gateway']==r2['gateway']):
						found=True
						changed+='/deleted1->'+d['gateway']
						break
				if(found): continue
				if(not ipconfig):
					out,err=subprocess.Popen('ipconfig', shell=True, stdout=subprocess.PIPE).communicate()
					out=out.decode()
					ipconfig=True
				if(out.find(' '+d['ip']+'\r')==-1 and out.find(' '+d['ip']+'\n')==-1): changed+='/deleted2->'+d['gateway']
				else: addRoutes.append(d)
			
		if(changed):
			print('route changes detected ('+changed+')')
			self.reset(addRoutes)
		
		self.after(routesCheckInterval*1000, self.check)
		
#-------------------------------------------

	def reset(self, addRoutes=None):
		self.container.destroy()
		self.createWidgets(addRoutes)

#-------------------------------------------
			
	def __init__(self, master=None):
		global config, configFile
		config=self.config=configparser.ConfigParser()
		configFile=os.path.dirname(os.path.realpath(__file__))+'\\config.ini'
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
