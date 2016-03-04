from alchemyapi import AlchemyAPI

KEY = open('./api_key.txt','rb').read()[:-1]


def alcObj():
        return AlchemyAPI(KEY)

obj = alcObj()
test_text = "Hello"

def sentAn(test_text):
	response = obj.sentiment("text", test_text)
	score 	 = response[u'docSentiment'][u'score']
	type	 = response[u'docSentiment'][u'type']
	return score, type



