import csv
import numpy as np
import requests
import scipy as sp
import sklearn as sl

import pandas as pd

GOOGLE_QUOTE_URL = "http://www.google.com/finance/getprices?f=d,o,h,l,c,v&df=cpct&i=60&q="
PATH = "./Det_DATA/"

def getHistory(symbol,company):
	filename = PATH + company + ".txt"
	try:
		file = open (filename, "a+")
	except:
		file = open (filename, "w+")

	stock_url = GOOGLE_QUOTE_URL + symbol
#	print stock_url
	r = requests.get(stock_url)
	file.write(r.text.encode('utf-8'))
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


