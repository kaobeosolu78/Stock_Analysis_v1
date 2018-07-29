import bs4,requests
import pickle
import numpy as np


#Given a stock ticker, scrapes return on equity data of the stocks industry from csimarket.com
def get_industry_roe(ticker):
    
    #Returns the name of a stocks industry given a ticker
    def get_ticker_industry(ticker):
        #webscraper
        rawindcode = requests.get(("https://csimarket.com/stocks/at_glance.php?code={}").format(ticker))
        rawcodesoup = bs4.BeautifulSoup(rawindcode.text, "html.parser")
        table = (rawcodesoup.find('table', {'class': 'Industry_tablica'}))

        code = (((str(((table).findAll("a"))[1]))[43:47]).replace("\"", ""))

        #webscraper
        rawindname = requests.get(("https://csimarket.com/Industry/Industry_Data.php?ind={}").format(code))
        rawnamesoup = bs4.BeautifulSoup(rawindname.text, "html.parser")
        td = (rawnamesoup.find('td', {'class': 'ch1'}))
        industry_name = (((((td).text)))[2:])
        return industry_name

    Industry_Name = ((str(get_ticker_industry(ticker)))[:-4])

    #Function for opening pickled files
    def load_obj(name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)

    #Each industry has a code number linked to it, another function was used to find the numbers and pickle them into a dictionary
    Industry_Name_Key = load_obj("Industry_Name_Key")
    
    
    key = Industry_Name_Key[Industry_Name]#Construction Raw Materials Industry
    industry_roe_array = np.empty((6, 4), float)
    years = ["", 4, 8, 12, 14, 18]  # 2018,2017,2016,2015,2014,2013,
    count = 0

    #webscraper
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
        
    #given equity which was acquired above, roe is calculated and put into an array
    def calc_ind_avg_roe(industry_roe_array):
        avg_industry_roe = []
        for i in range(6):
            temp = 0
            counter = 0
            for k in range(4):
                if industry_roe_array[i][k] == 0:
                    counter -= 1
                    pass
                else:
                    temp += industry_roe_array[i][k]
            avg_industry_roe.append(temp/(4+counter))
        return avg_industry_roe
    avg_industry_roe = calc_ind_avg_roe(industry_roe_array)

    return (industry_roe_array,avg_industry_roe,Industry_Name)

print (get_industry_roe("AAPL"))#Note: website seems to only have nyse tickers at the moment



