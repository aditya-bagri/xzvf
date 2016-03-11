import csv
import numpy as np
import requests
import scipy as sp
import sklearn as sl

import pandas as pd

import os
import os.path


INTERVAL = 60 #sec
GOOGLE_QUOTE_URL = "http://www.google.com/finance/getprices?f=d,o,h,l,c,v&df=cpct&i="+str(INTERVAL)+"&q="
PATH = "./Det_DATA/"

## This function collects detailed data from the Google Finance API
## for each Ticker symbol. It saves this data in a file named after the company 
## input. 
def getHistory(symbol,company):
	filename = PATH + company + ".csv"
	try:
		os.remove(filename)
	except:
		pass

	try:
		file = open (filename, "a+")
	except:
		file = open (filename, "w+")

	stock_url = GOOGLE_QUOTE_URL + symbol
	resp = requests.get(stock_url)
	resp_filter = resp.text.split(" ")
	
	## From 6 to exclude the textual information, upto -1 to exclude the last \n
	text_list = resp_filter[0].split("\n")[7:-1]
	file.write("TIME,CLOSE,HIGH,LOW,OPEN,VOLUME\n")
	for row in text_list: 
		file.write(row+"\n")
#	file.write(resp_filter)
	file.close()	

def main():
        reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
        company_list=[]
        sym_list=[]
        for sym in reader:
                company=sym["COMPANY"]
                symbol=sym["SYMBOL"]
                company_list.append(company)
                sym_list.append(symbol)
        print sym_list

        for i in range(0,len(sym_list)):
#		print sym_list[i]
                getHistory(sym_list[i], company_list[i])


main()


