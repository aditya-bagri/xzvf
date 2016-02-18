import yahoo_finance
from yahoo_finance import Share
import time
import csv
import os
import numpy as np

TIME_IN_MIN = 30 # min
TIME_BETWEEN_ITERATIONS = 30 #sec

def outlier (arr, number_of_std_devs):
	sig = np.std(arr)
	mu = np.mean(arr)
	outlier_val= number_of_std_devs*sig
	valid=[]
	outlier = []
	for elem in arr:
		if np.abs(elem - mu) <= outlier_val:
			valid.append(elem)
		else:
			outlier.append(elem)
	return valid, outlier

def clear_files():
         with open('Yahoo_symbols.csv','rb') as sym_list:
		reader = csv.DictReader(sym_list)
		if reader:
		    for sym in reader:
			PATH="./Q4_files/"+sym["COMPANY"]+".csv"
			try:
				os.remove(PATH)
#				print "Removing "+sym["COMPANY"]+".csv"
			except Exception, e:
				print "Error=", str(e)
				pass

def create_files():
        for i in range(0,TIME_IN_MIN*60/TIME_BETWEEN_ITERATIONS):
	    reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
     	    for sym in reader:

			company=sym["COMPANY"]
			symbol=sym["SYMBOL"]
			while(1):
			   try:
				share_name=Share(symbol)
				if share_name:
					break
			   except:
				time.sleep(1)
				#share_name=Share(symbol)

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

TEST_MODE=1
LIVE_MODE=0
def test_outlier(mode):
#	a = np.random.randint(-1500, 1500, 2500).astype(np.float64)+np.random.rand(1,2500)
	if mode:
		path = "./Q4_with_data/"
	else:
		path = "./Q4_files/"
#		main()
        reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
	price_arr=[]
        for row in reader:
		print row
                company=row["COMPANY"]
                symbol=row["SYMBOL"]
                while(1):
                           try:
                                share_name=Share(symbol)
                                if share_name:
                                        break
                           except:
                                time.sleep(1)

#                share_name=Share(symbol)
                filename = path+company+".csv"
                file=open(filename,"r+")
		price_arr=[]
		for line in file:
#			print line
		    try:
			price_arr.append(float(str(line).split(',')[1]))	
		    except:
			pass
		    val,out= outlier(price_arr,2)
		#price_arr=[]
		try:
			data_clean=open(path+company+"_cleaned.csv", 'w+')
		except:
			data_clean=open(path+company+"_cleaned.csv", 'a')
		data_clean.write("%s\nCleaned Data: %s\nOutliers: %s"%(company,val,out))
		data_clean.close()
		file.close()
		print "%s\nCleaned Data: %s\nOutliers: %s"%(company,val,out)

main()
test_outlier(LIVE_MODE)

### To do: 1. Update outlier Function
### 	   2. Run code LIVE
