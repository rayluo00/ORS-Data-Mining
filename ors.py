import json
import requests

def ORS_CurrentData ():
	itemID = '2434'

	ors_request = requests.get('http://api.rsbuddy.com/grandExchange?a=guidePrice&i='+itemID)
	itemData = ors_request.json()
	print(itemData)

def ORS_HistoricalData ():
	itemID = '2434'
	timeInterval = '60'
	startTime = '1474615279000'

	ors_request = requests.get('https://api.rsbuddy.com/grandExchange?a=graph&g='+timeInterval+
				'&start='+startTime+'&i='+itemID)
	itemData = ors_request.json()
	print(len(itemData))

if __name__ == '__main__':
	#ORS_CurrentData()
	ORS_HistoricalData()
