import numpy as np
import pickle

def load_data(ticker):
    def load_obj(ticker,datatype):
        with open("{}_{}_Data".format(ticker,datatype) + '.pkl', 'rb') as f:
            return pickle.load(f)
    [growth_rates, sum_quarterly_growth] = load_obj(ticker,"Revenue")
    [eps_data,growth_rate,share_data,cash_flow_data,change] = load_obj(ticker,"EPS")
    [annual_net_income,annual_roe,annual_equity,Industry_Name,avg_industry_roe] = load_obj(ticker,"ROE")

    return growth_rates,sum_quarterly_growth,eps_data,growth_rate,share_data,cash_flow_data,change,annual_net_income,annual_roe,annual_equity,Industry_Name,avg_industry_roe

[growth_rates,sum_quarterly_growth,eps_data,eps_growth,share_data,cash_flow_data,eps_quality,annual_net_income,annual_roe,annual_equity,Industry_Name,industry_roe] = load_data("TSLA")


def REV_analysis(growth_rates,sum_quarterly_growth):
    index = list(growth_rates.keys())
    growth = []
    growth_score = []
    sum_growth = []
    sum_growth_15_17 = []
    for ind in index:
        growth.append(growth_rates[ind])
        sum_growth.append(sum_quarterly_growth[ind])

    for k in range(5):
        sum_growth_15_17.append(sum((growth[k])[-2:]))


    if sum_growth_15_17[4] > 0 and np.std(sum_growth_15_17[:4]) < 8:
        print ("Negative Revenue Growth of {}% from 2015 to 2017".format((sum(sum_growth_15_17[:4]))/4))
        return False

    for k in range(4):
        if sum_growth_15_17[k] <= 0:
            growth_score.append(0)
        elif sum_growth_15_17[k] >= 0 and sum_growth_15_17[k] < 3:
            growth_score.append(1)
        elif sum_growth_15_17[k] >= 3 and sum_growth_15_17[k] < 8:
            growth_score.append(2)
        else:
            growth_score.append(3)

    if sum(growth_score) < 8:
        print ("Negative Revenue Growth of {}% from 2015 to 2017".format((sum(sum_growth_15_17[:4]))/4))
        return False
    else:
        print ("Positve Revenue Growth of {}% from 2015 to 2017".format((sum(sum_growth_15_17[:4]))/4))
        return True


def EPS_analysis(eps_quality,eps_growth):
    quarters = ["Quart 1", "Quart 2", "Quart 3", "Quart 4"]
    quarters_growth = ["Quart 1 Growth","Quart 2 Growth","Quart 3 Growth","Quart 4 Growth"]
    quality = []

    quality_values = [eps_quality[quarter] for quarter in quarters]
    growth = [eps_growth[quarter] for quarter in quarters_growth]

    for k in range(len(quality_values)):
        if quality_values[k] <= 0:
            quality.append(0)
        elif quality_values[k] > 0 and quality_values[k] <= 2:
            quality.append(1)
        elif quality_values[k] > 2 and quality_values[k] <= 4:
            quality.append(2)
        elif quality_values[k] > 8 and quality_values[k] <= 12:
            quality.append(3)
        else:
            quality.append(4)

    if sum(quality) < 11:
        print ("Warning: EPS of Poor Quality")


    if sum(growth)/len(growth) > 0:
        print ("Positive Average EPS Growth of {}%".format(sum(growth)/len(growth)))
        return True

    else:
        print ("Negative Average EPS Growth of {}%".format(sum(growth)/len(growth)))
        return False


def ROE_analysis(industry_roe,roe):#last three years
    index = list(roe.keys())
    difference = []
    for year in index:
        difference.append(roe[year]-industry_roe[year])
    if sum(difference)/len(index) < 2 and np.std(difference) < 10:
        print ("Average Return on Equity is {}% Less than its Industry Return from 2015 to 2017".format(sum(difference)/len(index)))
        return False
    else:
        print ("Average Return on Equity is {}% Greater than its Industry Return from 2015 to 2017".format(sum(difference)/len(index)))
        return True


#annual_roe = {2017: 36.86750846372038, 2016: 36.90328104554046, 2015: 46.24819187360872}
#industry_roe = {2018: 37.8625, 2017: 37.8625, 2016: 37.8625, 2015: 37.8625, 2014: 37.8625, 2013: 37.8625}
#eps_quality = {'Quart 1': 5.891599401378739, 'Quart 2': 1.613671824881476, 'Quart 3': 10.270493161379026, 'Quart 4': 7.548329056859458}
#eps_growth = {'Quart 1 Growth': 11.214953271028026, 'Quart 2 Growth': -26.206896551724128, 'Quart 3 Growth': -27.1356783919598, 'Quart 4 Growth': 59.199999999999996}


print (REV_analysis(growth_rates,sum_quarterly_growth))
print (EPS_analysis(eps_quality,eps_growth))
print (ROE_analysis(industry_roe,annual_roe))