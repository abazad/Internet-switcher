import subprocess
import time
import threading
import funcs

class Async(threading.Thread):
	def __init__(self, mainApp):
		threading.Thread.__init__(self)
		self.daemon=True
		self.mainApp=mainApp
	def run(self):
		while(True):
			time.sleep(3)
			routes=funcs.queryRoutes()
			if(self.mainApp.routes!=routes): print('!!!!')
			#print(self.mainApp.routes)
