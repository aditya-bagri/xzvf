import sys
import datetime as dt
import pandas as pd
import pandas.io.data as pio
from pandas import Series
from yahoo_finance import Share

def plotDiagram(company, today):
    df = pio.get_data_yahoo(
        company,
        start = dt.datetime(2015, 1, 1),
        end = dt.datetime(today.year, today.month, today.day))

    df.loc[today] = (Share(company).get_open(), Share(company).get_days_high(), Share(company).get_days_low(), Share(company).get_price(), Share(company).get_volume(), float(Share(company).get_price()))
    cprice = df['Adj Close']
    mavg = pd.rolling_mean(cprice, 10)
    ewma = pd.ewma(cprice, span = 3)
    print "Estimate Price of " + company + " @ " + str(today + dt.timedelta(days=1)) + ": "
#    print ("  Actual Price: "
#            + str(Share(company).get_historical(str(today), str(today)).pop(-1)['Adj_Close'])
#            + " @ " + str(today))
    print "  " + str(predictPrice(cprice, mavg, ewma))+ "\n"
#    print "  Analysis by data until " + str(today)

def predictPrice(CPRICE, MAVG, EWMA):
    gr = (1 - 5 ** 0.5) / 2
    return ((EWMA[-1] - EWMA[-2]) * (gr)
            + (MAVG[-1] - MAVG[-2]) * (1 - gr)
            + CPRICE[-1])

if __name__ == '__main__':
    firms = ['AXP', "T", 'BA', 'GE', 'NKE', 'GS', 'IBM', 'MSFT', 'MCD', 'WMT']
    today = dt.date.today()
    for company in firms:
        plotDiagram(company, today)

