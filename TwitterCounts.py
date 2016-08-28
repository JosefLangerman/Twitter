import tweepy
import time

#Handling the rate limit using cursors
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)








#Connecting to Twitter
consumer_key = "nq0mAEdNGMJxxdL5AKTfOCWuY"
consumer_secret = "wHEfT0JiJvtuAAfSU3H9CMPSF4aJfFTkXvyOmVPJrjyJHXPCpY"
access_token = "489735293-2lMVnL5BGzT0bG0v7qhQqg0FUuVLWLTfa5I4d1Q7"
access_token_secret = "Eaqlfy8cU6vEGqHa5rKISFm9nN9xUTd2M5hDHtht47MtP"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#=======================================



#twitter_user = twitterhandle.get_user('karlofuchs')



print("Hi there")

query_name = "karlofuchs"

followers = tweepy.Cursor(api.followers, screen_name=query_name).items()

while True:
    try:
        follower = followers.next()
        print(str(query_name)+', '+str(follower.screen_name))
    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue
    except StopIteration:
        break






#for follower in limit_handled(tweepy.Cursor(twitter_user.followers).items()):
#    if follower.friends_count < 300:
#        print (follower.screen_name)






#print (twitter_user.screen_name+', '+str(twitter_user.followers_count))
#for twitter_followers in twitter_user.followers():
#    print(friend.screen_name+' '+str(friend.followers_count))
#    print(twitter_user.screen_name+', '+str(twitter_followers.screen_name))





#print user.followers_count
#for friend in user.friends():
#   print friend.screen_name






#friends = tweepy.Cursor(api.friends, screen_name="karlofuchs").items()

#while True:
#    try:
#        friend = friends.next()
#        print(adam.screen_name+", "+friend.screen_name) 
#        g.add_edge(adam.screen_name, friend.screen_name)
#    except tweepy.TweepError:
#        time.sleep(60 * 15)
#        continue
#    except StopIteration:
#        break

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
