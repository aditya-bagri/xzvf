#######################################################
## Date: 11th of March, 2016
##
## Original Code by Maanit Mehra
##
## Code may be reproduced without prior permissions.
## 
## This code is part of the submission process for 
## Advanced Big Data, Spring '16.
## (HW2)
#######################################################

import sys
import datetime
import pandas as pd
import pandas.io.data as pio
from pandas import Series
import numpy as np
from numpy import dot as Dot
import csv

def get_company_list():
	reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
        company_list=[]
        sym_list=[]
        for sym in reader:
                company=sym["COMPANY"]
                symbol=sym["SYMBOL"]
                company_list.append(company)
                sym_list.append(symbol)
	return company_list, sym_list


def lin_regression(company_list):
     for company in company_list:
	today = datetime.date.today()
	
	## The Pandas dataframe utilises the yahoo finance APIs to extract the
	## data from the start to end of a point. Note: Unlike method1, 
	## this utilises only opening, closing price, highs & low prices from before the desired
	## date ranges & volume data. 
	## Also, unlike that method, we do not have a detailed source of data for custom minute-by-minute
	## data streams.
	dataframe = pio.get_data_yahoo(company,start = datetime.datetime(2015, 1,21), end = datetime.datetime(today.year,today.month,today.day))

	## The dataframe includes parameters including the Open, High, Low, Close, Volume & Adj Close fields. 

	## npMat --> numpy Matrix that can use the 
	## dataframe on a number of different tasks.
	npMat = dataframe.as_matrix()

	## We are establishing a training model that encompasses 
	## some training data, some test data & finally some validation
	## data. We use this to divide the training & test parts away from
	## the entire data collection.

	x = npMat[:-1,1:]
#	x = np.hstack (( np.ones(( np.size(x, axis=1), 1)), x  ))
	y = npMat[1:,0]

	## We use the Least Squares Regression Model,
	## based off of the standard min LS error approach.
	## w = (X^{T}X)^{-1}*X^{T}y
	xtx = Dot(x.T,x)
	xy  = Dot(x.T,y)
	try:
		w = Dot(np.linalg.inv(xtx), xy)
	except:
		## for singularity conditions
		w = Dot(np.linalg.pinv(xtx), xy)

	## Printing the w enables clarifying the relations between
	## inputs and outputs.
	print w

	## We select some test elements from within the matrix 
	## to choose a choice of test vectors.
	xtest = x[-1,:]
	ytestAct = y[-1]		## Test Output, to companre against
	ytestPred= Dot(xtest, w)	## Predicted Test Case output

	## Inputs that need to be measured to return the predictions
	x_pred = npMat[-1,1:]
	Fin_pred = Dot(x_pred,w)

	print "%s\tPred:%.2f\t"%(company, Fin_pred)


def main():
	company_name_list, company_list = get_company_list()
	lin_regression(company_list)

main()



