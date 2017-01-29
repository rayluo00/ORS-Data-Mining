'''
ors.py

Authors: Raymond Weiming Luo and Ben Ellerby
'''

import json
import time
import requests

##############################################################################################
'''

JSON Return Data:

{"Overall",
 "buying",
 "selling",
 "buying Quantity",
 "sellingQuantity",}
'''
def ORS_CurrentData ():
    itemID = '2434' # Item ID

    ors_request = requests.get('http://api.rsbuddy.com/grandExchange?a=guidePrice&i='+itemID)
    itemData = ors_request.json()
    print(itemData)

##############################################################################################
'''

JSON Return Data:

{"ts",
 "buyingPrice",
 "buyingCompleted",
 "sellingPrice",
 "sellingCompleted",
 "overallPrice",
 "overallCompleted",}
'''
def ORS_HistoricalData ():
    itemID = '2434'             # Item ID
    startTime = '1357027200000' # Unix start time (milliseconds)
    timeInterval = '30'         # Time interval (minutes), min = 30
    tracebackTime = 94670778000 # Traceback time (milliseconds)

    ors_request = requests.get('https://api.rsbuddy.com/grandExchange?a=graph&g='+timeInterval+
                                '&start='+startTime+'&i='+itemID)
    itemData = ors_request.json()
    print(len(itemData))

if __name__ == '__main__':
    #ORS_CurrentData()
    ORS_HistoricalData()
