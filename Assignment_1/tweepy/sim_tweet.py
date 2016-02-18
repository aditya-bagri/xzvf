import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
 
consumer_key = '6TqQz48URR9TB05aJrEJImGiV'
consumer_secret = '3rS565yVptdc0oiO7Qt9iyzHwQiyX0sjX5zXkWz2IPhZeDJp6i'
access_token = '312541120-TjWwfT5TDkAFK6fkMfNbgjChdsBRQuvMc8g5i6Q1'
access_secret = 'OY5Y4PzOzEzRUGdUHigKjTDyXqHOVZO89mykn1EK8WV0O'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['python'])
