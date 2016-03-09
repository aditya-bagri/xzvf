from alchemyapi import AlchemyAPI

KEY = open('../../api_key.txt','rb').read()[:-1]


def alcObj():
        return AlchemyAPI(KEY)


def sentAn(obj, text):
	response = obj.sentiment("text", text)
	print response
	try:
		score 	 = response[u'docSentiment'][u'score']
	except:
		score 	 = 0
	type	 = response[u'docSentiment'][u'type']
	return score, type

def testAlc():
	obj = alcObj()
	test_text_list = ["Donald Trump is papa smurf.","Aditya Bagri is in the house.", "Aditya Bagri is in the house!", "Donald Trump is PAPA SMURF!!"]
	for test_text in test_text_list:
		score, type = sentAn(obj, test_text)
		print "test_text:\t", test_text
		print "Sentiment is %s %s" %(str(score), str(type))

testAlc()
