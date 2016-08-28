import tweepy
import networkx as nx
import time
import matplotlib.pyplot as plt

#Consumer Key (API Key)	nq0mAEdNGMJxxdL5AKTfOCWuY
#Consumer Secret (API Secret)	wHEfT0JiJvtuAAfSU3H9CMPSF4aJfFTkXvyOmVPJrjyJHXPCpY

consumer_key = "nq0mAEdNGMJxxdL5AKTfOCWuY"
consumer_secret = "wHEfT0JiJvtuAAfSU3H9CMPSF4aJfFTkXvyOmVPJrjyJHXPCpY"
access_token = "489735293-2lMVnL5BGzT0bG0v7qhQqg0FUuVLWLTfa5I4d1Q7"
access_token_secret = "Eaqlfy8cU6vEGqHa5rKISFm9nN9xUTd2M5hDHtht47MtP"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print (tweet.text)

adam = api.get_user('karlofuchs')
# Models contain the data and some helper methods which we can then use:

g = nx.Graph()

print("Hi there")
friends = tweepy.Cursor(api.friends, screen_name="karlofuchs").items()

while True:
    try:
        friend = friends.next()
        print(adam.screen_name+", "+friend.screen_name) 
        g.add_edge(adam.screen_name, friend.screen_name)
    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue
    except StopIteration:
        break

#friends = tweepy.Cursor(api.friends, screen_name="RealGeneKim").items()

#while True:
#    try:
#        friend = friends.next()
#        g.add_edge(adam.screen_name, friend.screen_name)
#    except tweepy.TweepError:
#        time.sleep(60 * 15)
#        continue
#    except StopIteration:
#        break

#friends = tweepy.Cursor(api.friends, screen_name="joseflangerman").items()

#while True:
#    try:
#        friend = friends.next()
#        g.add_edge(adam.screen_name, friend.screen_name)
#    except tweepy.TweepError:
#        time.sleep(60 * 15)
#        continue
#    except StopIteration:
#        break

#print(g.edges())
#nx.draw(g)
