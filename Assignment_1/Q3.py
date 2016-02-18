import sys
from time import sleep
from datetime import datetime
import json
import tweepy

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

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Showing all new tweets for #programming:"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['IBM'])
