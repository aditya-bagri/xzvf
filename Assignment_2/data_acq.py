import csv
import math
import random
import numpy as np
import time
from yahoo_finance import Share
import os
import sys


TIME_BETWEEN_ITERATIONS=30 #sec
TIME_IN_MIN=135 #minutes
## A Function defined to clear out the files that may already be existing.
def clear_files():
         with open('Yahoo_symbols.csv','rb') as sym_list:
                reader = csv.DictReader(sym_list)
                if reader:
                    for sym in reader:
                        PATH="./DATA/"+sym["COMPANY"]+".csv"
                        try:
                                os.remove(PATH)
                        except Exception, e:
                                print "Error=", str(e)
                                pass

## A dummy outlier function created in Python. 
## Unused in this code. If required, however, can be easily 
## used as a substitute to the Spark function above.
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


## This function creates files and populates them with live data from the Yahoo Finance feed
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

                        filename = "./DATA/"+company+".csv"
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

## Precursor function calling the two functions above.
## Use this to clear out older files and create, populate the new ones.
def prepare_files(mode):
        if mode:
                clear_files()
        create_files()

CLEAR_FILES_ENABLE=1
CLEAR_FILES_DISABLE=0

def getData(mode):
        path = "./DATA/"
        prepare_files(mode)
        reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))

        ## Code below to select the files from a list of defined files.
        price_arr=[]
        for row in reader:
                print row
                company=row["COMPANY"]
                symbol=row["SYMBOL"]

                ## This while loop executes until valid data found
                ## Note that on some occasions the code below 
                ## may throw errors due to bad connections,
                ## hence the try...except condition is implemented.
                while(1):
                           try:
                                share_name=Share(symbol)
                                if share_name:
                                        break
                           except Exception,e:
				print e
				pass
                                time.sleep(1)
                ## Creating files for each company.
                ## Company list is stored externally.
                filename = path+company+".csv"
                file=open(filename,"r+")
                price_arr=[]

                ## For each file, find the cleaned data, outliers &
                ## store them in a file for each of the data points.

                for line in file:
                    try:
                        price_arr.append(float(str(line).split(',')[1]))
                    except:
                        pass
                    val,out= outlier(price_arr,2)
                try:
                        data_clean=open(path+company+"_cleaned.csv", 'w+')
                except:
                        data_clean=open(path+company+"_cleaned.csv", 'a')
                data_clean.write("%s\nCleaned Data: %s\nOutliers: %s"%(company,val,out))
                data_clean.close()
                file.close()
                print "%s\nCleaned Data: %s\nOutliers: %s"%(company,val,out)

getData(CLEAR_FILES_DISABLE)

