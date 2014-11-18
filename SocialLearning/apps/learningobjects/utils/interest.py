import unfurl
import urllib2
import json
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#####TWITTER KEYS#####
CONSUMER_KEY = 'ieZUZgZrSJJE0QLBBOsgXg'
CONSUMER_SECRET = 'PlIpSrh6unKYZISSDieBIFAB3D9f6aSh4p4Dmcn8Q'
OAUTH_TOKEN = '1015949947-0Akq5OBnEzTp7OwaIuvLNiKN6L52FNLVOW9yIyf'
OAUTH_TOKEN_SECRET = 'SJz3nXcyGt2lIKhmPiFg5VlTdHLbrRSPRRgUZ552xfe1e'
####Twitter auth handler####
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
twittApi = tweepy.API(auth)

# { u'StumbleUpon': 0, 
#   u'Reddit': 0, 
#   u'GooglePlusOne': 0, 
#   u'Pinterest': 0, 
#   u'Twitter': 0, 
#   u'Diggs': 0, 
#   u'LinkedIn': 0, 
#   u'Facebook': { u'commentsbox_count': 0, 
#                  u'click_count': 0, 
#                  u'total_count': 0, 
#                  u'comment_count': 0, 
#                  u'like_count': 0, 
#                  u'share_count': 0 }, 
#  u'Delicious': 0, 
#  u'Buzz': 0
# }

class Interest(object):


    def __init__(self):
        
        self.factores = {'LinkedIn': 2, 'Twitter': 2, 'Delicious':2 } 
        self.suma = sum(self.factores.values())
        for key in self.factores.keys():
            self.factores[key] = self.factores[key] / self.suma        

    def get_interest_count(self,url):
        response=urllib2.urlopen('http://free.sharedcount.com/?url='+url+'&apikey=cabec5c5d636b063cbbcf8cbe966fd3c4c7d9152')
        res=json.loads(response.read())
        return res

    def get_interest(self,url):

        data = self.get_interest_count(url)

        url_interest = 0
       
        for key in self.factores.keys():
            url_interest += data[key] * self.factores[key] / suma

        return url_interest 

    def get_count(self,url,social_network):
        print "hola"
        data=self.get_interest_count(url)
        to_pop=[]
        for sn in data:
            if sn not in social_network:
                to_pop.append(sn)
        for tp in to_pop:
            data.pop(tp)
        return data

    def get_followers_count(self,user,social_network):
        if social_network=="Twitter":
            s=twittApi
            res=s.get_user(user).followers_count
            return res

    def get_post_count(self,user,social_network):
        if social_network=="Twitter":
            s=twittApi
            res=s.get_user(user).statuses_count
            return res

    def get_post_by_user_for_tag(self,tag,social_network):
        if social_network=="Twitter":
            a=twittApi.search(q=tag,show_user=True)
            users={}
            for r in a:
                if r.user.screen_name not in users:
                    users[r.user.screen_name]=1
                else:
                    users[r.user.screen_name]+=1
            return users