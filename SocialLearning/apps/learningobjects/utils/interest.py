import unfurl
import urllib2
import json
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from learningobjects.utils.parsers import *

from learningobjects.utils.unfurl import expand_url
from urlunshort import resolve

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

import math

def sigmoid(x, x0, k):
    y = 1 / (1+ math.exp(-k*(x-x0)))
    return y

def adjust(x):
    y = 100 * sigmoid(x,85,0.06)
    return y

def dictsum(d):
    suma = 0
    for k, v in d.iteritems():
        if isinstance(v, dict):
            suma += dictsum(v)
        else:
            suma += v

class Interest(object):

    def clean(self, url):

        try:
            furl = expand_url(url)
        except:
            furl = url

        return furl

    def __init__(self, url):

        self.url = self.clean(url)

        self.factores = {'LinkedIn': 2, 'Twitter': 2, 'Delicious':2 } 
        self.suma = sum(self.factores.values())
        for key in self.factores.keys():
            self.factores[key] = self.factores[key] / self.suma        

    def get_interest_count(self):

        response=urllib2.urlopen('http://free.sharedcount.com/?url='+self.url+'&apikey=cabec5c5d636b063cbbcf8cbe966fd3c4c7d9152')
        res=json.loads(response.read())
        return res

    def get_interest(self):

        res = self.get_interest_count()

        url_interest = res['Twitter'] + res['Facebook']['total_count']
       
        #for key in self.factores.keys():
        #    url_interest += data[key] * self.factores[key] / suma

        return url_interest 
