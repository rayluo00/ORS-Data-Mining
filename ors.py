'''
ors.py

Authors: Raymond Weiming Luo and Ben Ellerby
'''

import json
import time
import math
import requests
import statistics

##############################################################################################
'''

JSON Return Data:

{"Overall",
 "buying",
 "selling",
 "buyingQuantity",
 "sellingQuantity",}
'''
def ORS_CurrentData ():
    itemID = '536' # Item ID

    ors_request = requests.get('http://api.rsbuddy.com/grandExchange?a=guidePrice&i='+itemID)
    itemData = ors_request.json()

def FiveNumSummary (scList, sz):

    if sz % 2 == 0:
        mid = sz / 2
        lowq = statistics.median(scList[:math.floor(mid-1)])
        hiq = statistics.median(scList[math.ceil(mid):])
    else:
        mid = int(math.ceil(sz/2))-1
        lowq = statistics.median(scList[:mid])
        hiq = statistics.median(scList[mid+1:])
    
    med = statistics.median(scList)

    print('min',scList[0],'\n'
            'q1',lowq,'\n'
            'median',med,'\n'
            'q3',hiq,'\n'
            'max',scList[sz-1],'\n')



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
    itemID = '536'
    startTime = '1357027200000'
    timeInterval = '30'
    itemDict = {}

    orsRequest = requests.get('https://api.rsbuddy.com/grandExchange?a=graph&g='+timeInterval+
                                '&start='+startTime+'&i='+itemID)
    itemData = orsRequest.json()
    sz = len(itemData)
    

    itemDict['sellingCompleted'] = []
    for i in range(sz):
        if 'sellingCompleted' in itemData[i]:
            itemDict['sellingCompleted'].append(itemData[i]['sellingCompleted'])

    itemDict['sellingCompleted'].sort()
    sclens = len(itemDict['sellingCompleted'])

    FiveNumSummary(itemDict['sellingCompleted'], sclens)

if __name__ == '__main__':
    #ORS_CurrentData()
    ORS_HistoricalData()
