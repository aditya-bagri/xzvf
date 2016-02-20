## Source Code Based on: 
## http://www.markhneedham.com/blog/2015/02/15/pythonscikit-learn-calculating-tfidf-on-how-i-met-your-mother-transcripts/
##
## http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
## Original Code by Maanit Mehra
##
## Submission as part of Assignment Submission for Advanced Big Data @ Columbia University
## 
##
## Original Code AUthor: 	Maanit Mehra
## Date:			18th Feb, 2016

import numpy as np
from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.clustering import KMeans, KMeansModel
import prepareQ2

sc=SparkContext()

## Defining a generic TFIDF function for our purposes.
def TFIDF(source, destination):

	if destination[-1] != '/':
		destination=destination+'/'
	## typically define the source message
	rdd=sc.wholeTextFiles(source).map(lambda (name,text): text.split())
	tf=HashingTF()
	tfVectors=tf.transform(rdd).cache()
	a = tfVectors.collect()
	# Storing the TF values above in individual files, one per link
	ind = 0
	for vector in a:
		dest_path = destination + "TF_%d"%ind + ".txt"
		ind = ind + 1
		file = open(dest_path,'w')
		file.write(str(vector))
		file.close()
	# Calculating IDF Values for each case.
	idf=IDF()
	idfModel=idf.fit(tfVectors)
	tfIdfVectors=idfModel.transform(tfVectors)
	# Writing TF-IDF values to a single file.
	file = open(destination+"TF-IDF.txt", 'w')
	file.write(str(tfIdfVectors.collect()))
	try:
		for i in range(0,100):
			print ""#Testing Printing"
	except KeyboardInterrupt:
		pass

def test_TFIDF():
	TFIDF("./Q2_files/Random_*text.txt", "./Q2_TFIDF")

def main():
	# prepareQ2.py contains the cleaning and prep work for the 
	# TF-IDF code in this file.
	prepareQ2.main()
	test_TFIDF()

main()
