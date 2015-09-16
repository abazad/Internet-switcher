import os
import re
import subprocess

def queryRoutes():
	
	if dummyTest: command='type "'+os.path.dirname(os.path.realpath(__file__))+'\dummy_routes.txt"'
	else: command='route print 0.0.0.0'

	p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	out,err=p.communicate()
	out=out.decode()

	result=re.findall('[ \t]+(0.0.0.0)[ \t]+(0.0.0.0)[ \t]+([0-9.]{7,})[ \t]+([0-9.]{7,})[ \t]+([0-9]+)', out)

	routes=[]
	for i in range(len(result)):
		routes.append({'gateway':result[i][2], 'metric':int(result[i][4]), 'metric2': int(result[i][4])})
	
	return routes
	