import yahoo_finance
from yahoo_finance import Share
import time
import csv
import os
import numpy as np

TIME_IN_MIN = 3 # min
TIME_BETWEEN_ITERATIONS = 60 #sec

def outlier (arr, number_of_std_devs):
	sig = np.std(arr)
	mu = np.mean(arr)
	outlier_val= number_of_std_devs*sig
	valid=[]
	outlier = []
	for elem in arr:
		if (elem >= (mu - outlier_val)) and (elem <= (mu + outlier_val)):
			valid.append(elem)
		else:
			outlier.append(elem)
	return valid, outlier

def clear_files():
         with open('Yahoo_symbols.csv','rb') as sym_list:
		reader = csv.DictReader(sym_list)
		if reader:
		    for sym in reader:
			PATH="/home/ubuntu/BigData/Assignment_1/Q4_files/"+sym["COMPANY"]+".csv"
			os.remove(PATH)


def create_files():
        for i in range(0,TIME_IN_MIN*60/TIME_BETWEEN_ITERATIONS):
	    reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
     	    for sym in reader:

			company=sym["COMPANY"]
			symbol=sym["SYMBOL"]
			share_name=Share(symbol)
			filename = "./Q4_files/"+company+".csv"
			try:
				file=open(filename,"a")
			except:
				file=open(filename,"w")
				file.write("Time,Price")

			timestamp = share_name.get_trade_datetime()
			price = share_name.get_price()
			writer = csv.DictWriter(file, fieldnames=["Time","Price"], delimiter=",", lineterminator="\n")
			writer.writerow({"Time":timestamp ,"Price":price})		
	    time.sleep(TIME_BETWEEN_ITERATIONS)	

        file.close()

def main():
	clear_files()
	create_files()


def test_outlier():
	a = np.random.randint(-1500, 1500, 2500).astype(np.float64)+np.random.rand(1,2500)
	val,out= outlier(a,2)
	print out

test_outlier()

### To do: 1. Update outlier Function
### 	   2. Run code LIVE
