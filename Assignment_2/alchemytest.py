from alchemyapi import AlchemyAPI

KEY = open('../../api_key.txt','rb').read()[:-1]


def alcObj():
        return AlchemyAPI(KEY)


def sentAn(obj, text):
	response = obj.sentiment("text", text)
	score 	 = response[u'docSentiment'][u'score']
	type	 = response[u'docSentiment'][u'type']
	return score, type

def testAlc():
	obj = alcObj()
	test_text = "Donald Trump is a smurf."
	score, type = sentAn(obj, test_text)
	print "test_text:\t", test_text
	print "Sentiment is %s %s" %(str(score), str(type))

testAlc()
