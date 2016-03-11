###########################################################################
### Algorithmic collaboration with 
### Zoltan Onodi-Szucs, Palash Matey, Rikin Mathur
### Aditya Bagri, Anubha Bhargava & Marshall Van Loon
###
###
### Original Code Portions by Maanit Mehra
###
### References:
### http://www.scientificpapers.org/wp-content/files/1134_How_to_use_Fibonacci_retracement_to_predict_forex_market.pdf
###
###
### This code was completed as part of Assignment 2 of the
### the Advanced Big Data class for the Spring 2016 Semester
###########################################################################

import csv
import numpy as np
import requests
import scipy as sp
import sklearn as sl

import pandas as pd

import os
import os.path


from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from scipy.interpolate import interp1d

INTERVAL = 1 #min
GOOGLE_QUOTE_URL = "http://www.google.com/finance/getprices?f=d,o,h,l,c,v&df=cpct&i="+str(INTERVAL*60)+"&q="
PATH = "./Det_DATA/"

TIME_START = 1451606400



## This function collects detailed data from the Google Finance API
## for each Ticker symbol. It saves this data in a file named after  
## the company input. 
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
	
	## From 7 to exclude the textual information, upto -1 to exclude the final \n
	text_list = resp_filter[0].split("\n")[7:-1]
	file.write("TIME,CLOSE,HIGH,LOW,OPEN,VOLUME\n")
	elem_list=[]
	ctr = 0
	for row in text_list: 
		row_elems= row.split(',')
		if row_elems[0] == u'30':
			elem_list.append(row_elems) 
			ctr = ctr + 1;
		file.write(row+"\n")
	file.close()	
	return elem_list, ctr

def cleanFile(symbol,company):
	filename = PATH + company + ".csv"
	file_cleaned = PATH + company +"_cleaned.csv"
        try:
                os.remove(file_cleaned)
        except:
                pass

	reader=csv.DictReader(open(filename,'rb'))
	time_list=[]
    	for col in reader:
        	time=col["TIME"]
		
		time_list.append(time)
	stamp = 0
	for time in time_list:	
		if 'a' in time:
			stamp= time[1:]
			time = str( int(time[1:]) - TIME_START )
		else:
			time = str(int(stamp) + int(time) - TIME_START)

def extrapol(x, y, x_new, degree):
	f2 = interp1d(x, y, kind='cubic')
	f = np.poly1d(np.polyfit(x, y, degree))
	y_new = f(x_new)
	return y_new
	
def main():
	global var
        reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
        company_list=[]
        sym_list=[]
        for sym in reader:
                company=sym["COMPANY"]
                symbol=sym["SYMBOL"]
                company_list.append(company)
                sym_list.append(symbol)
        print sym_list
	var = -6	
	degree = 1

	print "Predictions:"
        for i in range(0,len(sym_list)):
                elem_list, ctr = getHistory(sym_list[i], company_list[i])
		ctr_arr = range(0,ctr)
		clos_list = []
		for elem in elem_list:
			clos_list.append(float(elem[1]))
		clos_arr = np.array(clos_list)

		if sym_list[i] == 'TWTR' or 'TSLA':
			degree = 5
		else:
			degree = 1

#		print "%s:\t%.2f\t"%(sym_list[i], extrapol(ctr_arr, clos_arr, ctr, degree))

		print "Ac:%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f"%(sym_list[i],extrapol(ctr_arr, clos_arr, ctr, 1),extrapol(ctr_arr, clos_arr, ctr, 2),extrapol(ctr_arr, clos_arr, ctr, 3), 
		extrapol(ctr_arr, clos_arr, ctr, 4), extrapol(ctr_arr, clos_arr, ctr, 5))
		ctr = ctr + var
                print "Pr:%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\tACT:%.2f"%(sym_list[i],extrapol(ctr_arr, clos_arr, ctr, 1),extrapol(ctr_arr, clos_arr, ctr, 2),
		extrapol(ctr_arr, clos_arr, ctr, 3), extrapol(ctr_arr, clos_arr, ctr, 4), extrapol(ctr_arr, clos_arr, ctr, 5), clos_arr[var])
 				
main()


