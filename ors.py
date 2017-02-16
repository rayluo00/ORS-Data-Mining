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

def findQuartiles (scList, sz):
    if len(scList) % 2 == 0:
        mid = len(scList) / 2
        lowq = statistics.median(scList[:math.floor(mid-1)])
        hiq = statistics.median(scList[math.ceil(mid):])
    else:
        mid = int(math.ceil(len(scList)/2))-1
        print(math.ceil(len(scList)/2))
        lowq = statistics.median(scList[:mid])
        hiq = statistics.median(scList[mid+1:])
    
    med = statistics.median(scList)

    return med, lowq, hiq

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
            #print(itemData[i]['sellingCompleted'])
            itemDict['sellingCompleted'].append(itemData[i]['sellingCompleted'])

    itemDict['sellingCompleted'].sort()
    #print(itemDict['sellingCompleted'],'\n\n')
    d_len = len(itemDict['sellingCompleted'])
    med, lowq, hiq = findQuartiles(itemDict['sellingCompleted'], d_len)
    print('min',itemDict['sellingCompleted'][0],'\n'
            'max',itemDict['sellingCompleted'][d_len-1],'\n'
            'median',med,'\n'
            'q1',lowq,'\n'
            'q3',hiq,'\n')

if __name__ == '__main__':
    #ORS_CurrentData()
    ORS_HistoricalData()
