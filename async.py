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
			routes=self.mainApp.queryRoutes()
			#print('######################')
			#print(self.mainApp.routes0==routes)
			#print(self.mainApp.routes)
