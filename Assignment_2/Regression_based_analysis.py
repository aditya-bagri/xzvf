import sys
import datetime as dt
import pandas as pd
import pandas.io.data as pio
from pandas import Series
import numpy as np
from numpy import dot as Dot

company_list=["BAC", "C", "IBM", "AAPL", "GE", "T", "MCD", "NKE", "TWTR", "TSLA"]
for company in company_list:
	df = pio.get_data_yahoo(company,start = dt.datetime(2015, 1,21), end = dt.datetime(2016,3,11))
#	print df

	npMat = df.as_matrix()

	x = npMat[:-1,1:]
	y = npMat[1:,0]
	# Using a simple regrssion model
	xtx = Dot(x.T,x)
	xy  = Dot(x.T,y)
	try:
		w = Dot(np.linalg.inv(xtx), xy)
	except:
		w = Dot(np.linalg.pinv(xtx), xy)

	print w

	xtest = x[-1,:]
	ytestAct = y[-1]
	ytestPred= Dot(xtest, w)
	x_pred = npMat[-1,1:]
	Fin_pred = Dot(x_pred,w)
	print "%s\tPred:%.2f\t"%(company, Fin_pred)


