import pandas as pd
import numpy as np
import pandas_datareader as pdr
import json
import alpha_vantage
import requests
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline
from sklearn import linear_model

desired_width = 320
pd.set_option('display.width', desired_width)


def get_data(indexe,stock):
    products = {}

    API_URL = "https://www.alphavantage.co/query"
    #tickers = ["DJI"]#,"IXIC","NYA"]
    def get(index):
        dates = []
        close = []
        volume = []
        data = {
            "function": "TIME_SERIES_DAILY",
            "symbol": "{}".format(index),
            "outputsize": "full",
            "datatype": "json",
            "apikey": "3EME18KF9FCCJ6CI"
        }
        dub = ((requests.get(API_URL, params=data)).json())
        datees = ((dub["Time Series (Daily)"]).keys())
        for key in datees:
            temp = ((dub["Time Series (Daily)"])[key])["4. close"]
            close.append(temp)
            wemp = ((dub["Time Series (Daily)"])[key])["5. volume"]
            volume.append(wemp)
        for key in list(datees):
            dates.append(((datetime.datetime.strptime(key, "%Y-%m-%d"))))
        return dates,close,volume

    for index in indexe:
        [dates,close,volume] = get(index)
        products[index] = {"Dates":dates, "Close":close, "Volume":volume}
    products[stock+" stock"] = {"Dates":dates, "Close":close, "Volume":volume}

    return products

products = get_data(["DJI","IXIC"],"AAPL")

DJI = (products["DJI"])
IXIC = (products["IXIC"])
AAPL = (products["AAPL stock"])
print ("WTF")
print (DJI)
print (IXIC)
print (AAPL)

temp = (np.reshape(DJI["Close"],(len(DJI["Close"]),1)))
bemp = (np.reshape(AAPL["Close"],(len(AAPL["Close"]),1)))
lin = linear_model.LinearRegression()
model = lin.fit(temp,bemp)#DJI["Close"],AAPL["Close"])
print (model.intercept_)


def calculate_beta(products):
    DJI = (products["DJI"])
    IXIC = (products["IXIC"])
    AAPL = (products["AAPL stock"])

    close = []
    beta = []
    closing = []
    closer = [AAPL["Close"],DJI["Close"]]
    time_period = 1

    for cl in closer:
        bose = []
        [bose.append(100*(float(cl[k-1])/float(cl[k])-1)) for k in range(len(cl)) if k-1 != -1]
        close.append(bose)

    value = len(close[0])/time_period

    for k in range(time_period):
        avg = []
        temp = 0
        bemp = 0

        split_data = [(close[0])[int((k)*value):int((k+1)*value)],(close[1])[int(k*value):int((k+1)*value)]]

        for clo in split_data:
            avg.append(sum(clo)/len(clo))

        for k in range(len(split_data[0])):
            temp += ((split_data[0])[k] - avg[0])*((split_data[1])[k]-avg[1])
            bemp += ((split_data[1])[k]-avg[1])*((split_data[1])[k]-avg[1])


        covariance = temp/(len(split_data[0])-1)
        variance = bemp/len(split_data[1])
        print (covariance)
        beta.append(covariance/variance)
    return beta

#beta = (calculate_beta(products))

#plotly.offline.plot({"data": [go.Scatter(x=dates, y=beta)],
                     #"layout": go.Layout(title="hello world")},
                     #image='jpeg', image_filename='test')

def tag_data(products):
    index = list(products.keys())
    final = []
    print (products)
    for i in range(1,len(index)):
        diff = []
        if i != len(index)-1:
            closer = [(products["{}".format(index[i])])["Close"],(products["{}".format(index[len(index)-1])])["Close"]]
        else:
            break
        print ("dub")
        print ((products["{}".format(index[i])])["Close"])
        close = []
        temp = 0
        print ((closer))

        time_period = 5
        for cl in closer:
            bose = []
            print (cl)
            [bose.append(100*(float(cl[k-1])/float(cl[k])- 1)) for k in range(len(cl)) if k - 1 != -1]
            close.append(bose)

        value = len(close[0]) / time_period
        for b in range(time_period):
            split_data = [(close[0])[int((b)*value):int((b+1)*value)],(close[1])[int(b*value):int((b+1)*value)]]

            for t in range(len(split_data[0])):
                temp += ((split_data[0])[t]-(split_data[1])[t])
                print #(split_data[1][t]-split_data[1][t])
            diff.append(float(temp/len(split_data[0])))
        final.append(diff)
        print (final)

    return

print (tag_data(products))
