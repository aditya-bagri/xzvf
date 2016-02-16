import yahoo_finance
from yahoo_finance import Share
import time
import csv
import os

#subprocess.call(shlex.split('rm ./Q4_files/*.csv'))


with open('Yahoo_symbols.csv','rb') as sym_list:
		reader = csv.DictReader(sym_list)
		for sym in reader:
			PATH="/home/ubuntu/BigData/Assignment_1/Q4_files/"+sym["COMPANY"]+".csv"
			os.remove(PATH)

for i in range(0,4):
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
file.close()
