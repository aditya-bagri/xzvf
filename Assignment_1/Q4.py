### Author: 	Maanit Mehra
### Date:	18th Feb, 2016
### 
### Code created for Assignment 1 of Advanced Big Data
###
### This code picks up data, using the Yahoo Finance feeds, 
### detects outliers and removes them.
###
### Main Function can be called in either LIVE_MODE
### which executes a realtime pickup and cleaning operation
### or 
### TEST_MODE which uses the data collected from a previous run.
###

import yahoo_finance
from yahoo_finance import Share
import time
import csv
import os
import numpy as np
import math
from pyspark import SparkContext
import sys

TIME_IN_MIN = 30 # min
TIME_BETWEEN_ITERATIONS = 30 #sec

## Creating a spark context.
sc = SparkContext()

## removeOutliers, as the name suggests, cleans the data, removing outliers.
def removeOutliers(nums,number_of_std_devs):
        stats = nums.stats()
        sig = math.sqrt(stats.variance())
        cleaned= nums.filter(lambda x: math.fabs(x - stats.mean()) <= number_of_std_devs * sig)
        return cleaned

## arrOfOutliers, as the name suggests, creates a vector with stored outliers.
def arrOfOutliers(nums,number_of_std_devs):
        stats = nums.stats()
        sig = math.sqrt(stats.variance())
        outliers= nums.filter(lambda x: math.fabs(x - stats.mean()) > number_of_std_devs * sig)
        return outliers

## this outlier function was created with the spark code.
## We parallelize the data here and make use of it in our calculations.
def outlier(arr, number_of_std_devs):
        nums = sc.parallelize(arr)
        val = sorted(removeOutliers(nums,number_of_std_devs).collect())
        out = sorted(arrOfOutliers(nums,number_of_std_devs).collect())
        return val, out

## A dummy outlier function created in Python. 
## Unused in this code. If required, however, can be easily 
## used as a substitute to the Spark function above.
def python_outlier (arr, number_of_std_devs):
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

## A Function defined to clear out the files that may already be existing.
def clear_files():
         with open('Yahoo_symbols.csv','rb') as sym_list:
		reader = csv.DictReader(sym_list)
		if reader:
		    for sym in reader:
			PATH="./Q4_files/"+sym["COMPANY"]+".csv"
			try:
				os.remove(PATH)
			except Exception, e:
				print "Error=", str(e)
				pass
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

## Precursor function calling the two functions above.
## Use this to clear out older files and create, populate the new ones.
def prepare_files():
	clear_files()
	create_files()


TEST_MODE=1 	## Use this mode when working in post processing only
LIVE_MODE=0	## Yse this mode when looking to stream and clean live data.

def main(mode):
	if mode:
		path = "./Q4_with_data/"
	else:
		path = "./Q4_files/"
		prepare_files()
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
                           except:
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

main(LIVE_MODE)
