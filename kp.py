import requests
import time
from phue import Bridge

starttime=time.time()
red = 0
green = 25500
yellow = 12750
orange  = 5000
_sleep = 60 * 3


def present():
	b = Bridge('10.0.0.12')
	b.connect()
	b.get_api()
	color = None
	r=requests.get('https://iswa.gsfc.nasa.gov/IswaSystemWebApp/DatabaseDataStreamServlet?format=JSON&resource=CCMC-PREDICTED_KP&quantity=KP&duration=1')
	entries = r.json()[-26:]
	x = 0
	y = 0
	for i in entries:
		x+=float(i['KP'])
		y+=1
	mean = x/y
	if(mean < 2):
		color=green
	elif(mean >= 2 and mean < 3):
		color=yellow
	elif(mean >= 3 and mean < 4):
		color=orange
	elif(mean >= 4):
		color=red
	temp = b.get_group(1)
	print("Cycle every " + str(_sleep/60) + " min ------------------")
	print("		Changing color to: " + str(color))
	print("		The average KP is: " + str(mean))
	print("		Timestamps from " + str(entries[0]['timestamp']) + " to " + str(entries[-1]['timestamp']))
	print("		Defaults are as: Bri: " + str(temp['action']['bri']) + " sat: " + str(temp['action']['sat']) + " hue: " + str(temp['action']['hue']))

	b.set_group(1, 'bri', 0, transitiontime=24)
	time.sleep(2.5)
	b.set_group(1, 'sat', 255)
	b.set_group(1, 'hue', color) #Darken
	for i in range(0,3):
		b.set_group(1, 'bri', 255, transitiontime=5) # On
		time.sleep(0.6)
		b.set_group(1, 'bri', 0, transitiontime=5) # off
		time.sleep(0.6)

	b.set_group(1, 'bri', temp['action']['bri'], transitiontime=50)
	b.set_group(1, 'hue', temp['action']['hue'], transitiontime=50)
	b.set_group(1, 'sat', temp['action']['sat'], transitiontime=50) # Back on
	time.sleep(1)


try:
    while True:
        present()
        time.sleep(_sleep)
except KeyboardInterrupt:
    print('Manual break by user')
except Exception as e:
    print('Something else went wrong... Check logs.')
    print(e)