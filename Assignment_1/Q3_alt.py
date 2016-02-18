import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os

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


