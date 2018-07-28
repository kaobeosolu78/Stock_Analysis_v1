import requests,bs4
import re
import numpy as np
from datetime import datetime
import pickle
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates




def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def get_data(tickers):
    bemp = 0

    for ticker in tickers:
        if os.path.isfile("{}.pkl".format(ticker)) == True:
            temp = load_obj(ticker)
            print (ticker)
            print (temp)
            continue

    def Get_10k(tickers):
        filecodes = {}
        CIK = {}
        badticks = []

        for ticker in tickers:
            rawcik = requests.get(("https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany").format(ticker))
            ciksoup = bs4.BeautifulSoup(rawcik.text, "html.parser")
            try:
                CIK[ticker] = (((ciksoup.find(text="CIK").findNext("a")).text)[3:-26])
            except:
                badticks.append(ticker)
                continue

        for tick in badticks:
            tickers.remove(tick)

        for ticker in tickers:
            filecode = {}
            raw10k = requests.get(("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-K&dateb=&owner=exclude&count=80").format(CIK[ticker]))
            ksoup = bs4.BeautifulSoup(raw10k.text,"html.parser")

            tr = (((ksoup.find(class_="tableFile2"))).findAll("tr"))
            td = (((ksoup.find(class_="tableFile2"))).findAll("td"))

            for k in range(len(tr)):
                if ((tr[k]).find(class_="small")) != None:
                    temp = ((((tr[k]).find(class_="small")).text)[62:82])
                    if temp[-1] == "i":
                        temp = ((((tr[k]).find(class_="small")).text)[59:79])
                        if int(temp[11:13]) < 20:
                            filecode["20" + temp[11:13]] = temp.replace("-", "")
                        else:
                            filecode["19" + temp[11:13]] = temp.replace("-", "")
                    elif temp[0] == "c":
                        temp = ((((tr[k]).find(class_="small")).text)[69:86])
                        if int(temp[11:13]) < 20:
                            filecode["20" + temp[11:13]] = temp.replace("-", "")
                        else:
                            filecode["19" + temp[11:13]] = temp.replace("-", "")
                    elif temp[10] != "-" or temp[13] != "-":
                        continue
                    elif int(temp[11:13]) < 20:
                        filecode["20" + temp[11:13]] = temp.replace("-", "")
                    else:
                        filecode["19" + temp[11:13]] = temp.replace("-", "")
            filecodes[ticker] = filecode

        return CIK,filecodes


    [CIK,filecodes] = (Get_10k(tickers))###################################################

    wop = {}

    for ticker in tickers:
        print (ticker)
        products = {}
        tickcodes = filecodes[ticker]
        index = list(tickcodes.keys())
        bount = 0
        one_sheet = ["", ""]

        for ind in index:
            no = 0
            numba = 0
            print (ind)
            requet = []
            data = []
            counter = 0
            while numba <=7 and counter < 1:
                if one_sheet[0] != True:
                    numba += 1
                else:
                    numba = one_sheet[1]
                rawincome = requests.get(
                    ("https://www.sec.gov/Archives/edgar/data/{}/{}/R{}.htm").format(CIK[ticker], tickcodes[ind],numba))
                incomesoup = bs4.BeautifulSoup(rawincome.text, "html.parser")
                try:
                    tr = (incomesoup.find(class_="report").findAll("tr"))
                    old = 0
                    print (numba)
                except:
                    rawincome = requests.get(
                        ("https://www.sec.gov/Archives/edgar/data/{}/{}/d10k.htm").format(CIK[ticker], tickcodes[ind]))
                    incomesoup = bs4.BeautifulSoup(rawincome.text, "html.parser")
                    data = re.compile(sheet,re.IGNORECASE)
                    tr = []
                    t = (((incomesoup).findAll("b")))
                    [tr.append(bet.parent.parent.findNext("table")) for bet in t if bet.find(text=data) != None]
                    try:
                        tr = ((tr[0]).findAll("tr"))
                    except:
                        help = requests.get(
                            "https://www.sec.gov/Archives/edgar/data/{}/{}".format(CIK[ticker], tickcodes[ind]))
                        helpsoup = bs4.BeautifulSoup(help.text, "html.parser")
                        tr = ((helpsoup.findAll("tr")))
                        for t in tr:
                            wet = ((t.find("a")))
                            if wet.find(text=re.compile("10-k")) != None or wet.find(text=re.compile("10k")) != None:
                                grale = (wet.text)
                        if grale[-1] == "t":
                            break

                        rawincome = requests.get(
                            ("https://www.sec.gov/Archives/edgar/data/{}/{}/{}").format(CIK[ticker],
                                                                                              tickcodes[ind], grale))
                        incomesoup = bs4.BeautifulSoup(rawincome.text, "html.parser")
                        data = re.compile(sheet, re.IGNORECASE)
                        tr = []
                        t = (((incomesoup).findAll("b")))
                        [tr.append(bet.parent.parent.findNext("table")) for bet in t if bet.find(text=re.compile(data)) != None]

                    old = 1


                if bount < 1:
                    requet = []
                    for k in range(len(tr)):
                        if len(tr[k].findAll("td")) > 0:
                            requet.append(((((tr[k]).findAll("td"))[0]).text))

                    print (requet)
                    sheet = str((((tr[0]).findAll("strong"))[0]).text).replace("CONSOLIDATED ","")


                    for k in range(len(sheet)):
                        if sheet[k] == "-":
                            b = k
                    sheet = sheet[:b-1]

                    bata = (input("What data would you like from {}'s {}".format(ticker,(((tr[0]).findAll("strong"))[0]).text))).split(",")
                    bount += 1

                    if str(bata[len(bata)-1])[:4] == 'next':
                        try:
                            if type(int(str(bata[len(bata)-1])[4])) == int:
                                numba = int(str(bata[len(bata)-1])[4])-1
                        except:
                            pass
                        del(bata[len(data)-1])
                        bount -= 1
                        for dat in bata:
                            products[dat] = []
                        if len(list(products.keys())) > 0:
                            pass#.append(numba)
                        continue
                    elif len(list(products.keys())) == 0 and bount == 1:
                        one_sheet = [True,numba]##########################

                    for dat in bata:
                        products[dat] = []

                for dat in list(products.keys()):
                    prods = []

                    for k in range(len(tr)):
                        rawprods = []
                        if tr[0].find(text=re.compile("thousand",re.IGNORECASE)) != None:
                            factor = 1000
                        elif tr[0].find(text=re.compile("million",re.IGNORECASE)) != None:
                            factor = 1000000
                        else:
                            factor = 1
                        #print ((tr[k]).text)#.find(text=re.compile("^"+str(dat.replace("'","")+"$"), re.IGNORECASE))))
                        #print (dat)
                        if (tr[k].find(text=re.compile("^"+str(dat.replace("'","")+"$"), re.IGNORECASE))) != None:
                            #print ("yeet")
                            [rawprods.append(((((tr[k]).findAll("td"))[i]).text).replace("\n", "").replace("\xa0", "").replace("$","").replace("Â", "")) for i in range(len(((tr[k]).findAll("td"))))]
                            rawprods = list(filter(None,rawprods))
                            if len(rawprods) > 10:
                                for k in range(len(rawprods)):
                                    if rawprods[k] == dat:
                                        rawprods = rawprods[k:k+2]
                                        break
                            print (rawprods)
                            prods = (float((re.sub(r"[^.0-9]","",rawprods[1]))))
                            counter += 1

                    if counter == 0:
                        if no == 0:
                            numba = 0
                        elif no == 6:
                            print("Couldnt find that data")
                            del(products[dat])
                            bount -= 1
                            numba = 0
                            no = 0
                        one_sheet = ["", ""]
                        no += 1
                        continue


                    if prods != [] and old != 1:
                        try:
                            products[dat].append([prods,((((tr[1]).findAll("div"))[1]).text)])
                        except:
                            products[dat].append([prods,((((tr[0]).findAll("div"))[1]).text)])
                    elif old == 1:
                        products[dat].append([prods,'Sep. 29, ' + ind])


        pickle_out = open("{}.pkl".format(ticker), 'wb')
        pickle.dump((products), pickle_out, pickle.HIGHEST_PROTOCOL)
        pickle_out.close()

        wop[ticker] = products

    return (wop)


tickers = ["goog"]#["acn","aes","amg","a","gas","apd","agn","alle","all","altr","aee","axp","aig","amp","abc","aph","apc","aiv"]#['ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'AAP', 'AES', 'AET', 'AFL', 'AMG', 'A', 'GAS', 'APD', 'ARG', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT']#chk wix pbr ewz
print (get_data(tickers))

def process_data(ticker):
    products = {}
    raw = []
    datees = []
    dates = []
    count = 0
    data = load_obj(ticker)
    index = (list(data.keys()))
    for ind in index:
        raw.append(data[ind])
    [datees.append(k[1]) for k in raw[0]]
    for r in raw:
        temp = []
        [temp.append(k[0]) for k in r]
        products[index[count]] = temp
        count += 1
    for date in datees:
        dates.append(datetime.strptime(date,"%b. %d, %Y"))

    quick_components = {"one":"Inventor","two":"assets","three":"liabilities"}
    for quick_component in list(quick_components.values()):
        mo1 = re.compile(r"{}".format(quick_component))

        for ind in (index):
            if (mo1.search((ind))) != None:
                for qui in quick_components.keys():
                    if quick_components[qui] == quick_component:
                        products[qui] = products[ind]
    for ind in index:
        del(products[ind])

    return products,dates

def debt_identifier(ticker):
    quick_ratio = []
    [products,dates] = process_data(ticker)
    dates = matplotlib.dates.date2num(dates)
    print(products)

    for k in range(len(products["one"])):
        bemp = ((products["two"])[k]-(products["one"])[k])
        quick_ratio.append(bemp/(((products["three"])[k])))

    (plt.plot_date(dates,quick_ratio))
    plt.show(block=True)



#print (debt_identifier("aapl"))

def process_eps_data(ticker):
    quick_components = {"one":"Inventory","two":"Total assets","three":"Total liabilities"}
    [products,dates] = process_data(ticker)
    def calculate_growth_rate(array):
        growth_rates = []
        counter = 0
        growth_rate = {}
        barray = array[0]

        avg = sum(barray)/len(barray)

        for k in range(len(barray)):
            if k - 1 == -1 or barray[k - 1] == 0:
                pass
            else:
                temp = (((barray[k - 1] - barray[k]) / abs(barray[k])) * 100)
                growth_rate[(array[1])[k]] = temp
                print (temp)

        return (growth_rate,avg)

    for key in list(products.keys()):
        array = ["",""]
        array[0] = products[key]
        array[1] = dates

        [growth_rates,avg] = calculate_growth_rate(array)

        #PERat = []
        #for k in range(len(array[0])):
        #
        #    df = web.DataReader("TSLA", 'morningstar', (array[1])[k])
        #    temp = ((df["Close"])[0])
        #    PERat.append(temp/((array[0])[k]))
        #print (PERat)
        (plt.plot_date(list(growth_rates.keys()),list(growth_rates.values())))
        plt.suptitle('Growth in {}\'s {}'.format(quick_components[key],ticker))
        plt.xlabel('Dates')
        plt.ylabel('% Growth'.format(quick_components[key]))
        plt.show(block=True)

        return array,growth_rates,avg

#print (process_eps_data("aapl"))