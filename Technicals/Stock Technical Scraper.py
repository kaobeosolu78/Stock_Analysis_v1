import requests
import alpha_vantage
import time
import pickle
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay
import statistics


def load_obj(name):#stop loss magic**
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# API_URL = "https://www.alphavantage.co/query"
# #["spwr","qcom","slrc","p","alb","orcl","ge","ford","snap","rad"]
# indexe = ["rad"]
# rawprods = load_obj("stock_data")
#
#
#
# def get(index):
#     dates = []
#     close = []
#     volume = []
#     ope = []
#     data = {
#         "function": "TIME_SERIES_DAILY",
#         "symbol": "{}".format(index),
#         "outputsize": "full",
#         "datatype": "json",
#         "apikey": "3EME18KF9FCCJ6CI",
#         "retries": 10
#     }
#
#     try:
#         dub = ((requests.get(API_URL, params=data)).json())
#         datees = ((dub["Time Series (Daily)"]).keys())
#     except:
#         try:
#             dub = ((requests.get(API_URL, params=data)).json())
#             datees = ((dub["Time Series (Daily)"]).keys())
#         except:
#             print("time series error")
#
#             return rawprods
#
#     for key in datees:
#         temp = ((dub["Time Series (Daily)"])[key])["4. close"]
#         close.append(temp)
#         wemp = ((dub["Time Series (Daily)"])[key])["5. volume"]
#         volume.append(wemp)
#         zemp = ((dub["Time Series (Daily)"])[key])["1. open"]
#         ope.append(zemp)
#     for key in (datees):
#         dates.append((key))
#
#     return [dates, close, volume, ope]
#
#
# for index in indexe:
#     [dates, close, volume, ope] = get(index)
#     rawprods[index] = {"Dates": dates, "Close": close, "Volume": volume, "Open": ope}
#
# for ind in indexe:
#     temp = []
#     [temp.append((float(rawprods[ind]["Close"][k])-float(rawprods[ind]["Open"][k]))) for k in range(len(rawprods[ind]["Open"]))]
#     rawprods[ind]["Diff"] = temp
#
# for ind in indexe:
#     bose = []
#     [bose.append((float(rawprods[ind]["Close"][k-1])-float(rawprods[ind]["Close"][k]))/float(rawprods[ind]["Close"][k-1])) for k in range(len(rawprods[ind]["Close"])) if k-1 != 0]
#     rawprods[ind]["Close"] = bose
#
# print (list(rawprods.keys()))
# pickle_out = open("stock_data.pkl".format(ind), 'wb')
# pickle.dump(rawprods, pickle_out, pickle.HIGHEST_PROTOCOL)
# pickle_out.close()

# indexe = ['tgt', 'wmt', 'spwr', 'cgc', 'bby', 'amzn', 'nke', 'ntla', 'bac', 'cron', 'nok', 'unh', 'spwr', 'ua', 'fb', 'nwl', 'amd', 'jnj', 'aapl']
#
indexe = ["slrc","alb","orcl","ge","ford","snap","rad"]
 #

trade_dates = list(pd.date_range("2018-01-2", "2018-12-31", freq=BDay()))
trade_dates = trade_dates[::-1]

for ind in indexe:
    rawprods = load_obj("stock_data".format(ind))
    avg = {}
    avgg = {}
    std = [0]
    bavg = []
    ount = 0
    stds = {}
    while ount < len(trade_dates):
        # if (trade_dates[ount].day == 4 and trade_dates[ount].month == 7) or (trade_dates[ount].day == 24 and trade_dates[ount].month == 7)

        vol = 0
        print (ount)
        bear = int((rawprods[ind]["Dates"][len(rawprods[ind]["Dates"])-1])[0:4])
        savg = len(bavg)
        # print (ind)
        print (trade_dates[ount])
        k = -1
        while bear < 2018:
            if k == len(rawprods[ind]["Close"])-1:
                k = 0
                bear += 1
                bavg.append(0)
            k += 1

            # print (bear)
            if trade_dates[ount].day == datetime.datetime.strptime(rawprods[ind]["Dates"][k], "%Y-%m-%d").day and trade_dates[ount].month == datetime.datetime.strptime(rawprods[ind]["Dates"][k], "%Y-%m-%d").month and datetime.datetime.strptime(rawprods[ind]["Dates"][k], "%Y-%m-%d").year == bear:
                bavg.append(rawprods[ind]["Diff"][k])
                if rawprods[ind]["Diff"][k] < 0:
                    vol -= float(rawprods[ind]["Volume"][k])
                    bear += 1
                    k = 0
                else:
                    vol += float(rawprods[ind]["Volume"][k])
                    bear += 1
                    k = 0
        if savg == len(bavg):
            bavg.append(0)

        avg[trade_dates[ount]] = vol/1000000
        if len(bavg) == 0:
            avgg[trade_dates[ount]] = 0
        else:
            yemp = []
            std = [0]
            [yemp.append(sum(bavg[:q])/len(bavg[:q])) for q in range(len(bavg)+1) if len(bavg[:q]) != 0]
            avgg[trade_dates[ount]] = yemp
            [std.append(statistics.stdev(bavg[:q])) for q in range(len(bavg)+1) if len(bavg[:q]) != 0 and len(bavg[:q]) != 1]
            stds[trade_dates[ount]] = std
        vol = 0
        print (len(yemp))
        print (len(std))
        print (yemp)
        bavg = []
        ount += 1


    pickle_out = open("{}_stock_data.pkl".format(ind), 'wb')
    pickle.dump(([avgg,stds,avg]), pickle_out, pickle.HIGHEST_PROTOCOL)
    pickle_out.close()

