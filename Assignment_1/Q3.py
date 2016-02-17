import tweepy
import sys
from time import sleep
from datetime import datetime

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

top = api.home_timeline()[0].id
print "top: %s" %(top)
while True:
    l = api.home_timeline()
    if top != l[0].id:
        top = l[0].id
#       print "l[0]:  ", l[0]
        print 'New tweet recognized by Python at: %s' % str(datetime.now())
    sleep(61)

