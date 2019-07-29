# Phue Space Weather Alert
Updates Phillips Hue lighting system based on the current KP Value pulled from a NASA Web URL with JSON API ([Link](https://iswa.gsfc.nasa.gov/IswaSystemWebApp/DatabaseDataStreamServlet?format=JSON&resource=CCMC-PREDICTED_KP&quantity=KP&duration=1)).

   - Lights change every 3 minutes
   - Colors are not on a specific scale - random colors given according to the scale.
   - Uses prediction API URL rather than current.

## Usage
Import required packages
```python
import requests
import time
from phue import Bridge
```

Create a function that connects Hue Bridge and requests and convert the data into JSON
```python
def present():
	b = Bridge('10.0.0.12')
	b.connect()
	b.get_api()
	color = None
	r=requests.get('https://iswa.gsfc.nasa.gov/IswaSystemWebApp/DatabaseDataStreamServlet?format=JSON&resource=CCMC-PREDICTED_KP&quantity=KP&duration=1')
	entries = r.json()[-26:]
```

Apply if, elif or else analysis accordingly to understand the data!
```python
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
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
