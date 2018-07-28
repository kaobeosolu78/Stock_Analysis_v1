import requests,bs4
import re
import numpy as np
import pickle
import datetime
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

now = datetime(2018,1,2)
year = timedelta(days = 365)
month = timedelta(days = 30)

# gets raw revenue data######################
def revenue(ticker):
    quarters = ["Yearly Average"]
    def revenue_data(ticker):
        revenue = []
        revenue_label = []
        revenue_float = []
        rawrev = requests.get(("https://csimarket.com/stocks/single_growth_rates.php?code={}&rev").format(ticker))
        revenuesoup = bs4.BeautifulSoup(rawrev.text, "html.parser")
        td = (revenuesoup.findAll("tr",{"onmouseover":"this.className='bgplv'"}))



        for k in range(6):
            revenue = []

            tr = (td[k].findAll("td"))
            tab = [(t.findAll("span")) for t in tr if t!=None]

            revenue.append(tab[2:])
            for rev in revenue:
                for i in range(4):
                    revenew = []
                    if (len(str(rev[i]))) <= 44:
                        revenue_float.append(0)
                    elif (len(str(rev[i]))) > 20:
                        temp = (((str(rev[i])[35:(43-(51-len(str(rev[i]))))])).replace(',', ''))
                        tmep = (float(temp))
                        revenue_float.append(tmep)

            if k < 4:
                ([revenue_label.append((td[k].findAll("strong")[i]).text) for i in range(2)])


        for b in range(8):
            for j in range(13):
                if ((((now + month*j).date()).strftime("%B, %Y"))[:-6]) == revenue_label[b]:
                    revenue_label[b] = ((now + month*j).date())

        for k in range(1,9,2):
            quarters.append(revenue_label[k-1] + ": {}".format((revenue_label[k].strftime("%B, %Y"))[:-6]))

        if len(revenue_float) != 20:
            revenue_float = revenue_float[0:20]


        return revenue_float###scrapes and formats revenue
    revenue = revenue_data(ticker)

    def analyze_revenue(revenue):
        Quarter_1 = revenue[0:4]
        Quarter_2 = revenue[4:8]
        Quarter_3 = revenue[8:12]#revenue data by quarter
        Quarter_4 = revenue[12:16]
        Full_Year = revenue[16:20]
        Array = (np.array([Quarter_1,Quarter_2,Quarter_3,Quarter_4,Full_Year]))

        def calculate_growth_rate(Quarter):
            growth_rates = []
            check = []
            for k in range(4):
                if Quarter[k]==0:
                    check.append(k)
                    pass
                elif k-1 == -1 or Quarter[k-1]==0:
                    pass
                else:
                    temp = (((Quarter[k - 1] - Quarter[k]) / Quarter[k]) * 100)
                    growth_rates.append(temp)

            return (growth_rates)###calculates growth rates from revenue data

        growth_rates = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}#defines growth rate and sum dictionaries
        sum_quarterly_growth = {"Yearly Average":0,"Quarter 4":1,"Quarter 3":2,"Quarter 2":3,"Quarter 1":4}

        for k in range(5):
            temp = Array[k]
            growth_rates[k] = calculate_growth_rate(temp)
    #calculates growth rate

        for k in range(4):
            growth_rates[quarters[k+1]] = growth_rates.pop(k)
        growth_rates[quarters[0]] = growth_rates.pop(4)


        for quarter in quarters:
            sum_quarterly_growth[quarter] = (sum(growth_rates[quarter]))/len(growth_rates[quarter])#creates quarterly growth from sum of growth rates

        del sum_quarterly_growth["Quarter 2"]
        del sum_quarterly_growth["Quarter 1"]
        del sum_quarterly_growth["Quarter 3"]
        del sum_quarterly_growth["Quarter 4"]

        pickle_out = open("{}_Revenue_Data.pkl".format(ticker), 'wb')
        pickle.dump((growth_rates,sum_quarterly_growth), pickle_out, pickle.HIGHEST_PROTOCOL)
        pickle_out.close()

        return (growth_rates,sum_quarterly_growth)

    [growth_rates,sum_quarterly_growth] = analyze_revenue(revenue)

    print ("Quarterly Revenue Growth Rates")
    print (growth_rates)
    print ("Average Growth Rate by Quarter(last three years)")
    print (sum_quarterly_growth)

    return growth_rates,sum_quarterly_growth,revenue


#gets raw eps data###################
def eps(ticker):
    def eps_data(ticker):
        years = [""]#,4,8,12,14,18]#2018,2017,2016,2015,2014,2013,
        eps_array = np.empty((6,5), float)
        growth_rate_array = np.empty((6,4),float)
        share_data_array = np.empty((6,5), float)
        count = 0
        for year in years:
            raweps = requests.get(("https://csimarket.com/stocks/income.php?code={}&hist={}").format(ticker,year))
            epssoup = bs4.BeautifulSoup(raweps.text, "html.parser")
            table = (epssoup.findAll('table', {'class': 'osnovna_tablica_bez_gifa'}))
            tr = (table[1].findAll("tr",{"onmouseover":"this.className='bgplv'"}))
            rawprodseps = (tr[2].findAll("span"))
            rawprodshares = (tr[3].findAll("span"))

            eps_data = {4:"",3:"",2:"",1:"",0:""}
            share_data = {5: "", 4: "", 3: "", 2: "", 1: ""}
            for k in range(5):
                eps_data[k] = (float(((rawprodseps[k]).text).replace(",","")))


            def calculate_growth_rate(Quarter):
                growth_raters = []
                counter = 0
                growth_rates = {"Quart 1 Growth": "", "Quart 2 Growth": "","Quart 3 Growth": "", "Quart 4 Growth": ""}
                yeet = ["Quart 1 Growth", "Quart 2 Growth","Quart 3 Growth", "Quart 4 Growth"]
                quarters = ["Quart 1", "Quart 2", "Quart 3", "Quart 4"]

                for k in range(5):
                    if Quarter[k] == 0:
                        pass
                    elif k - 1 == -1 or Quarter[k - 1] == 0:
                        pass
                    else:
                        temp = (((Quarter[k - 1] - Quarter[k]) / abs(Quarter[k])) * 100)
                        growth_raters.append(temp)

                for yee in yeet:
                    growth_rates[yee] = growth_raters[counter]
                    counter += 1

                return (growth_rates)  ###calculates growth rates from revenue data

            growth_rate = calculate_growth_rate(eps_data)


            quarters = ["Quart 1", "Quart 2", "Quart 3", "Quart 4","Quart 1 prime"]
            growth_rate_quarters = {"Quart 1 Growth", "Quart 2 Growth", "Quart 3 Growth", "Quart 4 Growth"}

            counter = 0
            for quarter in quarters:
                eps_data[quarter] = eps_data.pop(counter)
                counter += 1

            for k in range(1,6):
                share_data[k] = (float(((rawprodshares[k]).text).replace(",","")))

            counter = 0
            for quarter in quarters:
                counter += 1
                share_data[quarter] = share_data.pop(counter)

            eps_array[count] = [eps_data[quarter] for quarter in quarters]
            growth_rate_array[count] = [growth_rate[quarter] for quarter in growth_rate_quarters]
            share_data_array[count] = [share_data[quarter] for quarter in quarters]
            count += 1

        return eps_data,share_data,growth_rate,eps_array,growth_rate_array,share_data_array



    def cash_flow_data(ticker):
        years = [""]#,4,8,12,14,18]#2018,2017,2016,2015,2014,2013,
        cash_flow_array = np.empty((6,5), float)
        count = 0
        for year in years:
            raweps = requests.get(("https://csimarket.com/stocks/cashflow.php?code={}&hist={}").format(ticker,year))
            cashsoup = bs4.BeautifulSoup(raweps.text, "html.parser")
            tr = (cashsoup.findAll("tr", {"onmouseover": "this.className='bgplv'"}))
            for k in range(len(tr)):
                strong = (tr[k].findAll("strong"))
                if len(str(strong)) > 5 and ((str(strong))[47]) == "O":
                    rawproducts = (tr[k].findAll("strong"))[1:7]

            cash_flow_data = {4: "", 3: "", 2: "", 1: "", 0: ""}
            for k in range(5):
                cash_flow_data[k] = ((float(((rawproducts[k]).text).replace(",",""))))

            quarters = ["Quart 1", "Quart 2", "Quart 3", "Quart 4","Quart 1 prime"]
            counter = 0
            for quarter in quarters:
                cash_flow_data[quarter] = cash_flow_data.pop(counter)
                counter += 1

            cash_flow_array[count] = [cash_flow_data[quarter] for quarter in quarters]
            count +=1

        return (cash_flow_data,cash_flow_array)

    def eps_cash_flow_analysis(cash_flow_data,eps_data,share_data):
        quarters = ["Quart 1", "Quart 2", "Quart 3", "Quart 4"]
        change = {"Quart 1": "", "Quart 2": "","Quart 3": "", "Quart 4": ""}
        count = 0

        for quarter in quarters:
            change[quarter] = (cash_flow_data[count]/share_data[count])-eps_data[count]
            count += 1

        return change

    [eps_data,share_data,growth_rate,eps_array,growth_rate_array,share_data_array] = eps_data(ticker)
    [cash_flow_data,cash_flow_array] = cash_flow_data(ticker)

    change = []
    for k in range(5):
        quarters = ["Quart 1", "Quart 2", "Quart 3", "Quart 4"]
        cps_array = np.empty((6,4), float)
        if k == 0:
            change = (eps_cash_flow_analysis(cash_flow_array[k],eps_array[k],share_data_array[k]))
            cps_array[k] = [change[quarter] for quarter in quarters]
        else:
            brange = (eps_cash_flow_analysis(cash_flow_array[k],eps_array[k],share_data_array[k]))
            cps_array[k] = [brange[quarter] for quarter in quarters]

    print ("Basic Net EPS")
    print (eps_data)
    print ("EPS Growth Rate")
    print (growth_rate)
    print ("Basic Shares Outstanding(mil)")
    print (share_data)
    print ("Net Operating Cash Flow")
    print (cash_flow_data)
    print ("EPS Quality")
    print (change)

    pickle_out = open("{}_EPS_Data.pkl".format(ticker), 'wb')
    pickle.dump((eps_data,growth_rate,share_data,cash_flow_data,change), pickle_out, pickle.HIGHEST_PROTOCOL)
    pickle_out.close()

    return change,cash_flow_data,eps_data,share_data,growth_rate,eps_array,growth_rate_array,share_data_array,cps_array#######


#gets raw equity data ####################
def equity(ticker):
    def income_equity_data(ticker):
        rawincome = requests.get(("https://csimarket.com/stocks/single_growth_rates.php?code={}&net").format(ticker))
        incomesoup = bs4.BeautifulSoup(rawincome.text, "html.parser")
        table = (incomesoup.findAll('table', {'class': 'osnovna_tablica_bez_gifa'}))
        tr = (table[0].findAll("tr", {"onmouseover": "this.className='bgplv'"}))

        income_array = np.empty((5,4),float)
        for k in range(5):
            jeezy = []
            for i in range(4):
                temp = ((tr[k]).findAll("span"))
                jeezy.append(float(((temp[i]).text).replace(",","").replace("-","0")))
            income_array[k] = jeezy

        years = {0:"",1:4,2:8,3:12,4:16}  # 2018,2017,2016,2015
        equity_array = np.empty((5,4),float)
        for k in range(5):
            rawequity = requests.get(("https://csimarket.com/stocks/balance.php?code={}&hist={}").format(ticker,years[k]))
            equitysoup = bs4.BeautifulSoup(rawequity.text, "html.parser")
            rawannualequity = requests.get(("https://csimarket.com/stocks/balance.php?code={}&annual").format(ticker))
            annualequitysoup = bs4.BeautifulSoup(rawannualequity.text, "html.parser")
            etr = (equitysoup.findAll("tr", {"onmouseover": "this.className='bgplv'"}))
            annualetr = (annualequitysoup.findAll("tr", {"onmouseover": "this.className='bgplv'"}))

            annual_equity = []
            [annual_equity.append(float(((((annualetr[len(annualetr)-1]).findAll("span"))[k]).text).replace(",", "").replace("-", "0"))) for k in range(4)]
            jeezy = []
            [jeezy.append(float(((((etr[len(etr)-1]).findAll("span"))[i]).text).replace(",","").replace("-","0"))) for i in range(1,5)]
            equity_array[k] = jeezy

        return (income_array,equity_array,annual_equity)# x = year, y = quarter --- x = quarter, y = year

    [income_array,equity_array,annual_equity] = (income_equity_data(ticker))

    def calculate_roe(income_array,equity_array,annual_equity):#most recent year may not be accurate do to net income not being reported
        annual_roe = {2017:0,2016:1,2015:2}
        annual_net_income = income_array[4][1:]
        years = [2017,2016,2015]
        counter = 0

        for year in years:
            annual_roe[year] = (annual_net_income[counter]/(((annual_equity[counter]+annual_equity[counter+1]))/2))*100
            counter += 1

        return annual_net_income,annual_roe

    [annual_net_income,annual_roe] = calculate_roe(income_array, equity_array, annual_equity)

    print ("Annual Net Income")
    print (annual_net_income)
    print ("Annual Return on Equity")
    print (annual_roe)
    print ("Annual Equity")
    print (annual_equity)

    def get_industry_roe(ticker):
        def get_ticker_industry(ticker):
            rawindcode = requests.get(("https://csimarket.com/stocks/at_glance.php?code={}").format(ticker))
            rawcodesoup = bs4.BeautifulSoup(rawindcode.text, "html.parser")
            table = (rawcodesoup.find('table', {'class': 'Industry_tablica'}))

            code = (((str(((table).findAll("a"))[1]))[43:47]).replace("\"", ""))

            rawindname = requests.get(("https://csimarket.com/Industry/Industry_Data.php?ind={}").format(code))
            rawnamesoup = bs4.BeautifulSoup(rawindname.text, "html.parser")
            td = (rawnamesoup.find('td', {'class': 'ch1'}))
            industry_name = (((((td).text)))[2:])
            return industry_name

        Industry_Name = ((str(get_ticker_industry(ticker)))[:-4])

        def load_obj(name):
            with open(name + '.pkl', 'rb') as f:
                return pickle.load(f)

        Industry_Name_Key = load_obj("Industry_Name_Key")

        key = Industry_Name_Key[Industry_Name]#Construction Raw Materials Industry
        industry_roe_array = np.empty((6, 4), float)
        years = ["", 4, 8, 12, 14, 18]  # 2018,2017,2016,2015,2014,2013,
        count = 0

        for year in years:
            rawindustryroe = requests.get(("https://csimarket.com/Industry/industry_ManagementEffectiveness.php?ind={}&hist={}").format(key,year))
            industryroesoup = bs4.BeautifulSoup(rawindustryroe.text, "html.parser")
            table = (industryroesoup.findAll('table', {'class': 'osnovna_tablica_bez_gifa'}))
            industry_name = industryroesoup.find("div",{"class","compnamec"})
            tr = (table[0].findAll("tr"))

            industry_roe = []
            for k in range(5):
                if ((((tr[6]).findAll("span"))[k]).text) == "-":
                    industry_roe.append(0)
                else:
                    industry_roe.append(float(((((tr[6]).findAll("span"))[k]).text).replace(",","").replace("-","").replace("%","")))
            industry_roe_array[count] = industry_roe[1:]
            count += 1
        def calc_ind_avg_roe(industry_roe_array):
            avg_industry_list = []
            avg_industry_roe = {2018:"",2017:"",2016:"",2015:"",2014:"",2013:""}
            years = [2018,2017,2016,2015,2014,2013]
            for i in range(6):
                temp = 0
                counter = 0
                for k in range(4):
                    if industry_roe_array[i][k] == 0:
                        counter -= 1
                        pass
                    else:
                        temp += industry_roe_array[i][k]
                avg_industry_list.append(temp/(4+counter))
            for year in years:
                count = 0
                avg_industry_roe[year] = avg_industry_list[count]
                count += 1

            return avg_industry_roe

        avg_industry_roe = calc_ind_avg_roe(industry_roe_array)

        print ("Average Return on Equity for the {}".format(Industry_Name))
        print (avg_industry_roe)

        return (industry_roe_array,avg_industry_roe,Industry_Name)###########

    [industry_roe_array,avg_industry_roe,Industry_Name] = get_industry_roe(ticker)

    pickle_out = open("{}_ROE_Data.pkl".format(ticker), 'wb')
    pickle.dump((annual_net_income,annual_roe,annual_equity,Industry_Name,avg_industry_roe), pickle_out, pickle.HIGHEST_PROTOCOL)
    pickle_out.close()

    return annual_net_income,annual_roe,annual_equity,Industry_Name,avg_industry_roe#######



tickers = ["AAPL"]
for ticker in tickers:
    print ("-------",ticker,"-------")
    (revenue(ticker))
    (eps(ticker))
    equity(ticker)
    print ("")



