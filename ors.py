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
import scipy.stats

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
def GetItemList (ls, param):
    itemLs = []

    for item in ls:
        if param in item and item[param] > 130000:
            itemLs.append(item[param])
        else:
            itemLs.append(0)

    return itemLs

##############################################################################################
def FiveNumSummary (ls):
    param = 'sellingCompleted'
    itemLs = GetItemList(ls, param)

    itemLs.sort()
    sz = len(itemLs)

    # Find lower and upper quartiles
    if sz % 2 == 0:
        mid = sz / 2
        lowq = statistics.median(itemLs[:math.floor(mid-1)])
        hiq = statistics.median(itemLs[math.ceil(mid):])
    else:
        mid = int(math.ceil(sz/2))-1
        lowq = statistics.median(itemLs[:mid])
        hiq = statistics.median(itemLs[mid+1:])
    
    med = statistics.median(itemLs)

    print('min',itemLs[0],'\n'
            'q1',lowq,'\n'
            'median',med,'\n'
            'q3',hiq,'\n'
            'max',itemLs[sz-1],'\n')

    # Calculate range to find outliers
    iqr = (hiq - lowq) * 1.5
    lowestq = lowq - iqr
    highestq = hiq + iqr

##############################################################################################
def SlopeEvaluation (ls):
    sc = 'sellingCompleted'
    sp = 'sellingPrice'
    bp = 'buyingPrice'
    bc = 'buyingCompleted'
    sz = len(ls)

    for i in range(1, sz):
        try:
            ts = (ls[i]['ts']-ls[i-1]['ts'])/60000
            ts2 = (ls[i+1]['ts']-ls[i]['ts'])/60000
            sslope = (ls[i][sc] - ls[i-1][sc])/ts
            bslope =  (ls[i][bc] - ls[i-1][bc])/ts
            sslope2 = (ls[i+1][sc] - ls[i][sc])/ts2
            bslope2 =  (ls[i+1][bc] - ls[i][bc])/ts2

            spslope = (ls[i][sp] - ls[i-1][sp])/ts
            bpslope = (ls[i][bp] - ls[i-1][bp])/ts
            spslope2 = (ls[i+1][sp] - ls[i][sp])/ts2
            bpslope2 = (ls[i+1][bp] - ls[i][bp])/ts2
            print('sell %.2f'%sslope,'| sp %.4f'%spslope,'| buy %.2f'%bslope,'| bp %.4f'%bpslope)
            print('sell %.2f'%sslope2,'| sp %.4f'%spslope2,'| buy %.2f'%bslope2,'| bp %.4f'%bpslope2,'\n')
        except Exception as e:
            print(end='')

##############################################################################################
def PlotData (ls):
    itemLs = []
    paramLs = ['buyingPrice', 'buyingCompleted', 'sellingPrice', 'sellingCompleted', 'overallPrice', 'overallCompleted']
    #paramLs = ['sellingCompleted', 'buyingCompleted']

    for param in paramLs: 
        itemLs = GetItemList(ls, param)

        sz = len(itemLs)
        xi = numpy.arange(0, sz)
        A = numpy.array([xi, numpy.ones(sz)])

        slope, intercept, r_value, p_value, stderr = scipy.stats.linregress(xi, itemLs)
        line = slope * xi + intercept
        pylab.plot(xi, itemLs, 'o', xi, line)
        pylab.xlabel('time')
        pylab.ylabel(param)
        pylab.savefig(param+'.png')
        print(slope,'|',intercept,'|',r_value,'|',p_value,'|',stderr)
        matplotlib.pyplot.close()
    #pylab.savefig('buy_sell_plot.png')

##############################################################################################
def PlotNormalDist (ls):
    param = 'sellingCompleted'
    itemLs = GetItemList(ls, param)

    mean = statistics.mean(itemLs)
    variance = statistics.variance(itemLs)
    sigma = math.sqrt(variance)

    fig = matplotlib.pyplot.figure()
    normDist = numpy.linspace(min(itemLs), max(itemLs), len(itemLs))
    matplotlib.pyplot.plot(matplotlib.mlab.normpdf(normDist, mean, sigma))
    matplotlib.pyplot.xlabel(param)
    fig.savefig(param+'_pdf.png', dpi=fig.dpi) 

##############################################################################################
def UnsupervisedAnomaly(ls):
    itemLs = []
    paramLs = ['sellingCompleted', 'buyingCompleted']

    for param in paramLs:
        itemLs = GetItemList(ls, param)


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
    itemID = '1515'
    #startTime = '1357027200000'
    startTime = str(1488614400000 - (86400000*28))
    timeInterval = '30'

    orsRequest = requests.get('https://api.rsbuddy.com/grandExchange?a=graph&g='+timeInterval+
                                '&start='+startTime+'&i='+itemID)
    itemData = orsRequest.json()
    sz = len(itemData)

    #FiveNumSummary(itemData)
    PlotData(itemData)
    #PlotNormalDist(itemData)
    #SlopeEvaluation(itemData)
    UnsupervisedAnomaly(itemData)

if __name__ == '__main__':
    #ORS_CurrentData()
    ORS_HistoricalData()
