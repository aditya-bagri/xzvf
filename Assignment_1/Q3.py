import sys
from time import sleep
from datetime import datetime
import json
import tweepy
import time
import csv

# Consumer keys and access tokens, used for OAuth  
consumer_key = 'quEn1nu9vvvi45UMzCzSbKWop'
consumer_secret = 'Cn8Coc479NgrCa94o1OPxC005O2GKFhScW3TeaxXqjZR3NvVxZ'
access_token = '3714319335-YM4pNKnGTIpMirQOHm48IvTrkWaYJPyhMvU6pZG'
access_token_secret = 'inweSwvxNamcCZoTdP4JSV69X6BDusjLPwKWUJKOZosWE'

# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication  
api = tweepy.API(auth)

RUNNING_TIME = 30 #in minutes

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    #CTR=0
    def __init__(self, runtime=1,company_list=['IBM', 'Google','Yahoo','Apple','Facebook']):
	self.time  =time.time()
	self.limit =runtime*60
	self.list = company_list

    def file_write(self, company,a):
	pass	

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
	#self.CTR = self.CTR + 1
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
	#print self.CTR
        try:
           a= '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
#	   print a
#	   print self.list
	   for sym in self.list:
 	       #print sym+ " is the company name"
	       filename = './Q3_files/'+sym+'.txt'
#	       print "Test:" + str(filename)
	       try:
		   file = open(filename,'a')
	       except:
		   file = open(filename,'w') 
	
	       for line in a.split(' '):
	       #        print line
			if sym.lower() in line.lower(): 
				print sym
				file.write(str(a)+"\n")

#	       file.truncate()
	       file.close()
#	       self.file_write(sym, a) 
        except Exception,e:
           print "Error: "+str(e)
           for sym in self.list:
               #print sym+ " is the company name"
               filename = './Q3_files/'+sym+'.txt'

           #print "ERROR: "#+self.list
           pass
	if (time.time()-self.time > self.limit):
		exit()
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    company_list=[]
    reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
    for sym in reader:
        	company=sym["COMPANY"]
                symbol=sym["SYMBOL"]
		company_list.append(company)

    print company_list    
    print "Showing all new tweets for #programming:"
    ibm = StdOutListener(runtime=RUNNING_TIME, company_list=company_list)

    try: 	
   	stream = tweepy.Stream(auth, ibm)
    	stream.filter(track=company_list, languages=['en'])
    except KeyboardInterrupt:
  	pass
