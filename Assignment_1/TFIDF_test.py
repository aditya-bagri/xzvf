## Source Code Based on: 
## http://www.markhneedham.com/blog/2015/02/15/pythonscikit-learn-calculating-tfidf-on-how-i-met-your-mother-transcripts/
##
## http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
## Original Code by Maanit Mehra
##
## Submission as part of Assignment Submission for Advanced Big Data @ Columbia University

import numpy as np
from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.clustering import KMeans, KMeansModel

def TFIDF(source, destination):

	if destination[-1] != '/':
		destination=destination+'/'
	## typically define the source message
	sc=SparkContext()
	rdd=sc.wholeTextFiles(source).map(lambda (name,text): text.split())
	tf=HashingTF()
	tfVectors=tf.transform(rdd).cache()
	a = tfVectors.collect()

	ind = 0
	for vector in a:
		dest_path = destination + "TF_%d"%ind + ".txt"
		ind = ind + 1
		file = open(dest_path,'w')
		file.write(str(vector))
		file.close()
#	print "TF VECTORS.COLLECT():\n\n\n",tfVectors.collect()
	idf=IDF()
	idfModel=idf.fit(tfVectors)
	tfIdfVectors=idfModel.transform(tfVectors)
	#tfIdfVectors.saveAsTextFile("./Q2_TFIDF_vectors/Random_%f_TFIDF.txt"%np.random.rand())
#	print "IDBUCKTHISSHIT:\n\n\n", tfIdfVectors.collect()
	file = open(destination+"TF-IDF.txt", 'w')
	file.write(str(tfIdfVectors.collect()))
	try:
		for i in range(0,100):
			print ""#Testing Printing"
	except KeyboardInterrupt:
		pass

def test_TFIDF():
	TFIDF("./Q2_files/Random_*text.txt", "./Q2_TFIDF")

test_TFIDF()
