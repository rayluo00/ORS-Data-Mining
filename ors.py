'''
ors.py

Authors: Raymond Weiming Luo and Ben Ellerby
'''

import json
import time
import math
import requests
import numpy
import statistics
import matplotlib
matplotlib.use('Agg')
import pylab

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

##############################################################################################
def FiveNumSummary (ls, sz):

    # Find lower and upper quartiles
    if sz % 2 == 0:
        mid = sz / 2
        lowq = statistics.median(ls[:math.floor(mid-1)])
        hiq = statistics.median(ls[math.ceil(mid):])
    else:
        mid = int(math.ceil(sz/2))-1
        lowq = statistics.median(ls[:mid])
        hiq = statistics.median(ls[mid+1:])
    
    med = statistics.median(ls)

    print('min',ls[0],'\n'
            'q1',lowq,'\n'
            'median',med,'\n'
            'q3',hiq,'\n'
            'max',ls[sz-1],'\n')

    # Calculate range to find outliers
    iqr = (hiq - lowq) * 1.5
    lowestq = lowq - iqr
    highestq = hiq + iqr

##############################################################################################
def SlopeEvaluation (ls, sz):

    for i in range(1, sz):
        slope = ls[i] - ls[i-1]
        print(slope)

def LinearRegression (ls, sz):
    xi = numpy.arange(0,9)
    A = numpy.array([xi, numpy.ones(9)])
    y = [19,20,20.5,21.5,22,23,23,25.5,24]
    w = numpy.linalg.lstsq(A.T,y)[0]

    line = w[0]*xi*w[1]
    pylab.plot(xi,line,'r-',xi,y,'o')
    pylab.savefig('linear_reg.png')

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
    itemLs = []
    param = 'sellingCompleted'

    orsRequest = requests.get('https://api.rsbuddy.com/grandExchange?a=graph&g='+timeInterval+
                                '&start='+startTime+'&i='+itemID)
    itemData = orsRequest.json()
    sz = len(itemData)
    
    for i in range(sz):
        if param in itemData[i]:
            itemLs.append(itemData[i][param])

    itemLs.sort()
    sclens = len(itemLs)

    #FiveNumSummary(itemLs, sclens)
    #SlopeEvaluation(itemLs, sclens)
    LinearRegression(itemLs, sclens)

if __name__ == '__main__':
    #ORS_CurrentData()
    ORS_HistoricalData()
