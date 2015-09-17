import time
import threading

class Async(threading.Thread):
	def __init__(self, mainApp):
		threading.Thread.__init__(self)
		self.daemon=True
		self.mainApp=mainApp
	def run(self):
		while(True):
			time.sleep(3)
			routes2=self.mainApp.queryRoutes()
			routes1=self.mainApp.routes
			changed=False
			if(len(routes1) and routes1[0]['stat']=='del'):
				if(len(routes2)): changed=True
			elif(len(routes2)!=len(routes1)): changed=True
			else:
				for i in range(len(routes2)):
					if(routes2[i]['gateway']!=routes1[i]['gateway']):
						changed=True
						break
			if(changed): print('routes changed!')
			