# Stock_Analysis
The various programs contained in this repository utilize elements of python and other python modules to perform both fundamental and technical analysisis of stocks. The fundamental data originally was webscraped from csimarket.com, but various inconveniences caused me to switch to the Edgar SEC databank. Files titled "Form 10-k" contain information such as the balance sheet, cash flow statements, and income statements on every company that files taxes in America can be found in this databank. The one problem is that each 10-k is multiple pages long, making it incredibly tedious to sort through manually. Currently, the fundamental section of this repository is capable of parsing the edgar data tree and print the available selection of fundamental data. The user may then choose what data they would like, and the program goes through the rest of the tree copying that data to an array. Currently only a few choices for analysis available, however there is a lot of room for growth and the SEC's vast library of fundamental data provides many options for looking into the history of a company.



The technical data is acquired as arrays containing the close, open, volume and date of a stock for any day in the history of its existence. Recently sources of daily stock price data have been depreciating, so Alpha Vantage is one of my last options in obtaining the aforemtioned data. The technical section of this repository is responsible for recieving this data and for each day on the calendar calculating the historical average price increase percentage, the standard deviation of the percent increase and the volume. This is done for each year beginning on the year of the stocks release, days with a negative average growth and decrease in volume are dropped, and finally the results are graphed by standard deviation size. This shows what days relative to the stocks history you are most likely to make a gain listed in order of likeliness. These individual dates are then ran through my stock simulater program, and the actual gains are graphed 



Sources:
Edgar- https://www.sec.gov/edgar/searchedgar/companysearch.html
CSIMarket- https://csimarket.com
AlphaVantage- https://www.alphavantage.co
