import json
import requests

def ORS_Data ():
	ors_request = requests.get('http://api.rsbuddy.com/grandExchange?a=guidePrice&i=2434')
	itemData = ors_request.json()
	print(itemData)

if __name__ == '__main__':
	ORS_Data()
