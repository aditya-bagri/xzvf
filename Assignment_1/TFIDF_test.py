## Source Code Based on: 
##http://www.markhneedham.com/blog/2015/02/15/pythonscikit-learn-calculating-tfidf-on-how-i-met-your-mother-transcripts/
##
## http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/

import numpy as np
#import findspark
#findspark.init()
from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.clustering import KMeans, KMeansModel

sc=SparkContext()
rdd=sc.wholeTextFiles("./Q2_files/*_text.txt").map(lambda (name,text): text.split())
tf=HashingTF()
tfVectors=tf.transform(rdd).cache()
idf=IDF()
idfModel=idf.fit(tfVectors)
tfIdfVectors=idfModel.transform(tfVectors)
tfIdfVectors.saveAsTextFile("./Q2_TFIDF_vectors/*.txt")


try:
	for i in range(0,100):
		print "Testing Printing"
except KeyboardInterrupt:
	pass
