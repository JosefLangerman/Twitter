import tweepy
import time
import os
import sys
import json
import argparse
import codecs
from tweepy.error import TweepError



FOLLOWING_DIR = 'following'
MAX_FOLLOWERS = 200
FOLLOWERS_OF_FOLLOWERS_LIMIT = 200

if not os.path.exists(FOLLOWING_DIR):
    os.mkdir(FOLLOWING_DIR)

#enc = lambda x: x.encode('ascii', errors='ignore')

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = 'nq0mAEdNGMJxxdL5AKTfOCWuY'
CONSUMER_SECRET = 'wHEfT0JiJvtuAAfSU3H9CMPSF4aJfFTkXvyOmVPJrjyJHXPCpY'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = '489735293-2lMVnL5BGzT0bG0v7qhQqg0FUuVLWLTfa5I4d1Q7'
ACCESS_TOKEN_SECRET = 'Eaqlfy8cU6vEGqHa5rKISFm9nN9xUTd2M5hDHtht47MtP'

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def get_follower_ids(centre, max_depth=1, current_depth=0, taboo_list=[]):

    # print 'current depth: %d, max depth: %d' % (current_depth, max_depth)
    # print 'taboo list: ', ','.join([ str(i) for i in taboo_list ])
    


    if current_depth == max_depth:
        print ('out of depth')
        return taboo_list

    if centre in taboo_list:
        # we've been here before
        print ('Already been here.')
        return taboo_list
    else:
        taboo_list.append(centre)

    try:
        userfname = os.path.join('twitter-users', str(centre) + '.json')
        
        if not os.path.exists(userfname):
            print ('Retrieving user details for twitter id %s' % str(centre))
            while True:
                try:
                    print('0')
                    print(centre) 
                    user = api.get_user(centre) 
                    #user = api.get_user(centre)
                    print('1')
                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'followers_ids': user.followers_ids()}
                    print('1.5')
                    with open(userfname, 'w', encoding="latin-1", errors="backslashreplace") as outf:
                        outf.write(json.dumps(d, indent=1))
                    print('2')
                    user = d
                    break
                except TweepError as error:
                    print('3') 
                    print (type(error))
                    

                    print(error.args[0][0]) 
                    if error.args[0][0] != 'N' and error.args[0][0] != 'F':
                        error_code = error.args[0][0]['code'] 
                    else:
                        error_code = 0
                    
                    print('4')
                    if error_code == 179:
                        print ('Can''t access user data - not authorized.')
                        return taboo_list

                    if error_code == 63:
                        print ('User suspended.')
                        return taboo_list
                    print('4.5')
                    if error_code == 88:
                        print ('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue

                    return taboo_list
        else:
            print('we go here')

            with open(userfname) as jsondata:
                user = json.loads(jsondata.read())

           # user = json.loads(file(userfname).read())

        #screen_name = enc(user['screen_name'])
        screen_name=user['screen_name']
        
        fname = os.path.join(FOLLOWING_DIR, str(screen_name) + '.csv')
        #print (fname)
        followerids = []

        # only retrieve friends of TED... screen names
        print(screen_name)
        if True:
 #       if screen_name.startswith('K'):
            print("Got here")
            if not os.path.exists(fname):
                print ('No cached data for screen name "%s"' % screen_name)
                with open(fname, 'w', encoding = "latin-1", errors="backslashreplace") as outf:
                    params = (user['name'], screen_name)
                    print ('Retrieving followers for user "%s" (%s)' % params)

                    # page over friends
                    c = tweepy.Cursor(api.followers, id=user['id']).items()

                    follower_count = 0
                    while True:
                        try:
                            follower = c.next()
                            followerids.append(follower.id)
                            params = (follower.id, follower.screen_name, follower.name)
                            outf.write('%s\t%s\t%s\n' % params)
                            follower_count += 1
                            if follower_count >= MAX_FOLLOWERS:
                                print ('Reached max no. of followers for "%s".' % follower.screen_name)
                                break
                        except tweepy.TweepError:
                            # hit rate limit, sleep for 15 minutes
                            print ('Rate limited. Sleeping for 15 minutes.')
                            time.sleep(15 * 60 + 15)
                            continue
                        except StopIteration:
                            break
            else:
                print('shit is here')
                with open(fname, 'r', encoding = "latin-1", errors="backslashreplace") as inputf:
                    followerids = [int(line.strip().split('\t')[0]) for line in inputf]

                #friendids = [int(line.strip().split('\t')[0]) for line in file(fname)]

            print('Found %d followers for %s' % (len(followerids), screen_name))

            # get friends of friends
            cd = current_depth
            if cd+1 < max_depth:
                for fid in followerids[:FOLLOWERS_OF_FOLLOWERS_LIMIT]:
                    taboo_list = get_follower_ids(fid, max_depth=max_depth,
                        current_depth=cd+1, taboo_list=taboo_list)

            if cd+1 < max_depth and len(followerids) > FOLLOWERS_OF_FOLLOWERS_LIMIT:
                print ('Not all followers retrieved for %s.' % screen_name)

    except Exception as error:
        print ('Error retrieving followers for user id: ', centre)
        print (error)

#        if os.path.exists(fname):
#            os.remove(fname)
 #           print ('Removed file "%s".' % fname)

        sys.exit(1)

    return taboo_list

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
    ap.add_argument("-d", "--depth", required=True, type=int, help="How far to follow user network")
    args = vars(ap.parse_args())



    twitter_screenname = args['screen_name']
    depth = int(args['depth'])

    if depth < 1 or depth > 3:
        print ('Depth value %d is not valid. Valid range is 1-3.' % depth)
        sys.exit('Invalid depth argument.')

    print ('Max Depth: %d' % depth)
    matches = api.lookup_users(screen_names=[twitter_screenname])

    if len(matches) == 1:
        print (get_follower_ids(matches[0].id, max_depth=depth))
    else:
        print ('Sorry, could not find twitter user with screen name: %s' % twitter_screenname)
