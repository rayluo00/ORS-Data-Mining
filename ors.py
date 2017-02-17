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
import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

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
def FiveNumSummary (ls):
    param = 'sellingCompleted'
    itemLs = []

    for item in ls:
        if param in item:
            itemLs.append(item[param])

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
        if sc in ls[i] and sc in ls[i-1] and bp in ls[i] and bp in ls[i-1]:
            ts = (ls[i]['ts']-ls[i-1]['ts'])/60000
            sslope = (ls[i][sc] - ls[i-1][sc])/ts
            bslope =  (ls[i][bc] - ls[i-1][bc])/ts
            print('sell slope %.2f'%sslope,'| c sell',ls[i][sp],'| p sell',ls[i-1][sp],
                    '\nbuy slope %.2f'%bslope,'| c buy',ls[i][bp],'| p buy',ls[i-1][bp],'\n')

##############################################################################################
def SendEmail ():
    img_data = open('linear_reg.png', 'rb'.read())
    msg = MIMEMultipart()
    msg['Subject'] = 'Linear Regression Graph'
    #msg['From']
    #msg['To']
    
    s = smtplib.SMTP(server, port)
    s.send_message(msg)
    print('email sent.')
    s.quit()

##############################################################################################
def LinearRegression (ls):
    itemLs = []
    param = 'sellingCompleted'

    for item in ls:
        if param in item:
            itemLs.append(item[param])

    sz = len(itemLs)
    xi = numpy.arange(0, sz)
    A = numpy.array([xi, numpy.ones(sz)])
    w = numpy.linalg.lstsq(A.T, itemLs)[0]

    line = w[0] * xi + w[1]
    pylan.xlabel('time')
    pylab.ylabel(param)
    pylab.plot(xi, line, 'r-', xi, itemLs, 'o')
    pylab.savefig('linear_reg.png')
    #SendEmail()

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

    orsRequest = requests.get('https://api.rsbuddy.com/grandExchange?a=graph&g='+timeInterval+
                                '&start='+startTime+'&i='+itemID)
    itemData = orsRequest.json()
    sz = len(itemData)

    #FiveNumSummary(itemData)
    PlotData(itemData)
    SlopeEvaluation(itemData)
    #LinearRegression(itemData)

if __name__ == '__main__':
    #ORS_CurrentData()
    ORS_HistoricalData()
