import pandas as pd
import numpy as np
import pandas_datareader as pdr
import json
import alpha_vantage
import requests
from scipy import stats
import quandl
import datetime
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as goo
import plotly.offline
from sklearn import linear_model
import pickle
from pandas.tseries.offsets import BDay
import statistics
import pandas_market_calendars as mcal
import time
from workalendar import usa
import os.path



def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def stock_sim(best, investment,y,ps):
    yaers = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999]
    close = ps["Diff"]
    dates = ps["Dates"]
    prods = []
    days = []
    dub = 0
    factor = investment
    fred = investment
    pred = 0

    for k in range(len(close)):
        prods.append([datetime.datetime.strptime(dates[k],"%Y-%m-%d"), close[k]])

    for prod in prods:
        if prod[0].month == best[0].month and prod[0].day == best[0].day and (prod[0].year == yaers[y]):  # or prod[0].year == 2017 or prod[0].year == 2016):
            days.append(prod)
            dub += 1


    for day in days:
        if day[1] < -3:
            chg = -3
        else:
            chg = (day[1])

    if (dub) == 0:
        return [0,fred-factor]
    return [chg,best[2]]

def analyze_data(index):
    pss = load_obj("stock_data")

    def organize_data(ind,y,ps,data):
        yaers = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999]
        optimal = {}

        avgs = data[0]
        stdraw = data[1]
        volume = data[2]

        bat = []
        dat = []
        std = []
        for k in range(len(list(avgs.keys()))):
            dat.append([(list(avgs.keys()))[k], (list(stdraw.values())[k])[len(list(stdraw.values())[k])-y-1], ((list(avgs.values()))[k])[len(list(stdraw.values())[k])-y-1], (list(volume.values()))[k]])
        [std.append(dat[d][1]) for d in range(len(dat))]

        fin = []
        for i in range(len(dat)):
            mi = min(std)
            [fin.append(dat[k]) for k in range(len(dat)) if mi == dat[k][1]]#sorts std by size
            for k in range(len(std)):
                if std[k] == mi:
                    del (std[k])
                    break


        for b in range(len(fin)):

            if (fin[b][1] == 0 and fin[b][2] == 0 and fin[b][3] == 0):
                (fin[b]) = None
        fin = list(filter(None, fin))

        return fin


    def optimize_std(ind,inv,optimal,y,ps):
        print (y)
        gain = []
        do = []
        full = []
        analysis = []
        set = 0
        std = []
        din = []
        sin = []
        det = 0
        bo = []
        vol = []

        for go in optimal:
            std.append(go[1])
            gain.append((stock_sim(go,inv,y,ps))[0])
            do.append((stock_sim(go,inv,y,ps))[1])
            bo.append(go[0])#fixxxxxxxxxxxx
            vol.append(go[3])

        for z in range(len(optimal)):
            predicted_gain = [(z,do[z],bo[z],gain[z],std[z],vol[z])]
            analysis.append(predicted_gain)

        full.append(analysis)

        return analysis
    for ind in index:
        ps = pss[ind]
        data = load_obj("{}_stock_data".format(ind))
        print (ind)
        answer = int(ps["Dates"][len(ps["Dates"])-1][2:4])
        if answer > 19:
            ery = 18
        else:
            ery = 18 - answer

        print (ery)

        scrub = [optimize_std(ind,1000,organize_data(ind,y,ps,data),y,ps) for y in range(ery-1)]
        print (scrub)

        pickle_out = open("{}_Analysis.pkl".format(ind), 'wb')
        pickle.dump((scrub), pickle_out, pickle.HIGHEST_PROTOCOL)
        pickle_out.close()

    return

def visualize(index,y):

    for ind in index:

        yaers = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999]
        if os.path.isfile("{}_Analysis.pkl".format(ind)) == False:
            analyze_data(["{}".format(ind)])

        analysis = (load_obj("{}_Analysis".format(ind)))
        try:
            analysis = analysis[y]
        except:
            continue
        avg_gain = []
        num = []
        opt = []
        avg_predicted_gains = []
        predicted_gains = []
        gains = []
        trash = []
        vol = []
        prediction = []
        top = []
        dates = []

        for k in range(len(analysis)):
            if (analysis[k][0][5]) > -100000 and ((datetime.date(yaers[y],analysis[k][0][2].month,analysis[k][0][2].day).weekday()) != 5 and (datetime.date(yaers[y],analysis[k][0][2].month,analysis[k][0][2].day).weekday()) != 6):
                num.append(analysis[k][0][0])
                gains.append(analysis[k][0][3])
                predicted_gains.append(analysis[k][0][1])
                dates.append(analysis[k][0][2])
                opt.append(analysis[k][0][4])
                vol.append(analysis[k][0][5])

        brains = gains
        predicted_brains = predicted_gains
        std = []
        growth = []
        for t in range(len(num)):
            std.append(opt[t])

        gains = goo.Line(x=[datetime.datetime.strftime(k, "%d/%m/%Y") for k in sorted(dates[:50])],y=gains[:50],name="gains")
        std = goo.Line(x=[datetime.datetime.strftime(k, "%d/%m/%Y") for k in sorted(dates[:50])],y=std[:50],name="std")
        predicted_gains = goo.Line(x=[datetime.datetime.strftime(k, "%d/%m/%Y") for k in sorted(dates[:50])],y=predicted_gains[:50],name="predicted_gains")
        volume = goo.Bar(x=[datetime.datetime.strftime(k, "%d/%m/%Y") for k in dates],y=vol,name="volume")

        fig = tools.make_subplots(rows=2, cols=1, subplot_titles=("{} gains {}".format(ind,yaers[y]), "std"))
        fig.append_trace(gains, 1, 1)
        fig.append_trace(predicted_gains,1, 1)
        fig.append_trace(std, 2, 1)

        # plotly.offline.plot({"data": fig,
        #                            "layout": goo.Layout(title="{}".format(ind))})

        prods = []
        brods = []
        k = -1
        datees = sorted(dates)
        for dat in sorted(dates):
            k = -1
            while k < len(dates) - 1:
                k += 1
                if dates[k] == dat:
                    prods.append(brains[k])
                    brods.append(predicted_brains[k])
                    break

        print("alpha")
        print(len(prods))
        print(sum(prods))
        print(datees)

        [slope, intercept, r_value, p_value, std_err] = stats.linregress(prods,brods)
        print (r_value)

        if sum(prods) > -111110:
            plotly.offline.plot({"data": [goo.Scatter(x=datees, y=prods, name="Actual Gains {}".format(2018 - y)),goo.Scatter(x=datees, y=brods, name="Predicted Gains {}".format(2018 - y))],
                                 "layout": goo.Layout(title="{} Gains {}: ${} per share in {} days".format(ind, 2018 - y, sum(prods),len(prods)))})


    return #datees,prods,predicted_brains

# for y in range(5):
    # (analyze_data(["aapl","tsla","wmt","unh"],y))
(visualize(["ua"],1))#"spwr","qcom","slrc", 'amzn', 'nke', 'ntla', 'bac', 'cron', 'nok', 'unh', 'spwr', 'ua', 'fb', 'nwl', 'amd', 'jnj', 'aapl',"tsla","cgc","unh","bby","nke","bac","amzn","nwl","amd","ua","nflx"],y))

#['tsla', 'ua', 'fb', 'nwl', 'amd', 'jnj','aapl']
    # ,"alb","orcl","ge","ford","snap","rad"],y))



