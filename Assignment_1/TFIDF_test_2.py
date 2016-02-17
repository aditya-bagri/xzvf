import math
from textblob import TextBlob as tb
#from future import division

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist)) -math.log(float (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

bloblist=[]
for i in range (0, 100):
	file = open ("./Q2_files/Random_%d_text.txt"%i, 'r+')
	a = file.read().decode('utf-8')
#	print "a:\n", a
	bloblist.append(tb(a))

#print bloblist[0]
for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("Word: {}, TF-IDF: {}".format(word.encode('utf-8'), score))
