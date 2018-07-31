# Stock_Analysis  W.I.P
The programs contained in this repository utilize elements of python and various python modules to perform both fundamental and technical analysisis on different stocks. Each program runs separately right now, but I plan on combining all of it with a master script once the different components are finished. Until then, each program takes as an input a list of tickers and will output the data either in the form of an array of data or as a dictionary of pickled values.    

Fundamental:

The fundamental data originally was webscraped from csimarket.com, but various inconveniences caused me to switch to the Edgar SEC databank. In this databank can be fount files titled "Form 10-k" which contain information such as the balance sheet, cash flow statements and income statements on every company that files taxes in America. This data is incredibly useful for looking into how at how a company manages its money, the one decider of its financial future however each 10-k can be hundreds of pages long, making it incredibly tedious to sort through the data for even one company. Currently, the fundamental section of this repository is capable of parsing the edgar data tree and printing out the available selection of fundamental data. The user may then choose what data they would like, and the program goes through the rest of the tree copying that data from every year into an array. Currently only a few choices for analysis exist, however there is a lot of room for growth there since the SEC's vast library of fundamental data provides many options for looking into the history of a company. In the near future I plan on adding more fundamental indicators to analysis and coupling this program with the technical analysis program. This will allow me to analyze historically any stocks that fit a certain criteria preset for growth in any fundamental category.


Technical:

The technical data is acquired as arrays containing the close, open, volume and date of a stock for any day in the history of its existence. Recently sources of daily stock price data have been depreciating, so Alpha Vantage is one of my last options in obtaining the aforemtioned data. The technical section of this repository is responsible for recieving this data and for each day on the calendar calculating the historical average price increase percentage, the standard deviation of the percent increase and the volume. This is done for each year beginning on the year of the stocks release, days with a negative average growth and decrease in volume are dropped, and finally the results are graphed by standard deviation size. This shows what days relative to the stocks history you are most likely to make a gain and how much gain is predicted to be made listed in order of descending probability. These individual dates are then put through my stock simulater function, and the actual gains are graphed alongside the predicted gains with the summed actual gain displayed on top. Just from the few stocks that I have analyzed, I have noticed gains of nearly ninety percent if the days calculated to have the best statistical chance of making a gain are traded, while other stocks are much better traded with a different strategy than the one my program employs.



Sources:
Edgar- https://www.sec.gov/edgar/searchedgar/companysearch.html
CSIMarket- https://csimarket.com
AlphaVantage- https://www.alphavantage.co
