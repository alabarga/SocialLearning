#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from learningobjects.utils import feedfinder
import feedparser
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import urllib2
import hashlib
import json
import re
from urlunshort import resolve
from django.core.management import call_command



class SocialNetworkAPI(object):

    def __init__(self, name):
        self.name = name

    def available_apis():
        return ['twitter', 'delicious']

    def clean(self,url):
        furl=url
        i=0
        while resolve(url)!=None and i<5:
            furl=url
            url=resolve(url)
            i+=1
            print i
        return furl


class Twitter(SocialNetworkAPI):

    def __init__(self):

        #####TWITTER KEYS#####
        CONSUMER_KEY = 'ieZUZgZrSJJE0QLBBOsgXg'
        CONSUMER_SECRET = 'PlIpSrh6unKYZISSDieBIFAB3D9f6aSh4p4Dmcn8Q'
        OAUTH_TOKEN = '1015949947-0Akq5OBnEzTp7OwaIuvLNiKN6L52FNLVOW9yIyf'
        OAUTH_TOKEN_SECRET = 'SJz3nXcyGt2lIKhmPiFg5VlTdHLbrRSPRRgUZ552xfe1e'
        ####Twitter auth handler####
        auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
        self.api = tweepy.API(auth)

        super(Twitter, self).__init__("twitter")

    def find_mentions(self,url):
        res = API.search(q=url)

    def get_expand(url,user,tag,):
        tagl=[]
        tagl.append(str(tag))
        relatedToTweet=[]        

        print"----------------------------"
        print "En twitter para el usuario "+user+" y tag "+str(tag)+": "
        response=twittApi.user_timeline(screen_name=user,count=10)
        for tweet in response:
            ht=extract_hash_tags(tweet.text)           
            intersect=list(set(tagl) & set(ht))
            if len(intersect)>0:
                #relatedToTweet.append(tweet)
                ##mirar si en el texto hay enlaces
                ##para cada enlace dle texto
                links= extract_urls(tweet.text.encode('utf-8'))
                for link in links:
                    link=resolve(link)
                    if link!=url:
                        print link
                        print "Fecha: "+str(tweet.created_at)
                        #call_command('add',URL=link)
                        feed=feedfinder.feed(link)
                        print feed
                        if feed: 
                            rc=ResourceContainer.objects.get_or_create(rss=feed,url=link)
                            add_feed(feed)
        print "__________________________"
            print ""
      

# code: b4d2325534966ff16094e19d5b23146a
# clientId: 4269302d99c97fd93d143d78bd7c4592
# secret: e6965b38674a3bcc9223783c01d638bf

#http://feeds.delicious.com/v2/json/url/b6da855510dae1a87aad452fbbda4245?key=4269302d99c97fd93d143d78bd7c4592

#curl https://avosapi.delicious.com/api/v1/posts/compose?url=http%3A%2F%2Foffbeat.topix.com%2Fstory%2F12646&_=1416161708256


#https://avosapi.delicious.com/api/v1/oauth/token?client_id=f5dad5a834775d3811cdcfd6a37af312&client_secret=7363879fee6c3ab0f93efbd24111ad34&grant_type=code&code=fa746b2eb266cab06f34fb7bc3d51160

# curl 'https://avosapi.delicious.com/api/v1/posts/compose?url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2F3D_printing&_=1416161708273' -H 'Origin: https://delicious.com' -H 'Accept-Encoding: gzip,deflate' -H 'Accept-Language: es-419,es;q=0.8,ca;q=0.6,de;q=0.4,en;q=0.2,eu;q=0.2,fr;q=0.2,gl;q=0.2,pt;q=0.2,ru;q=0.2' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/38.0.2125.111 Chrome/38.0.2125.111 Safari/537.36' -H 'Accept: ' -H 'Referer: https://delicious.com/link/950a4f5dd102ccbc371cbeea1c9a7c31' -H 'Cookie: company_history=%5B%5B%22http%3A//support.delicious.com/delicious%22%2C%22Delicious%22%5D%5D; avid=1kwyiwaz2b4rdxfdwnsbzbs8l; optimizelyEndUserId=oeu1414888627893r0.4138932339847088; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%222128660043%22%3A%222087051005%22%7D; __qca=P0-390458789-1416134340213; __utma=249254418.1030079492.1319781868.1416134868.1416161047.573; __utmc=249254418; __utmz=249254418.1416161047.573.3.utmcsr=programmableweb.com|utmccn=(referral)|utmcmd=referral|utmcct=/api/del.icio.us; _ga=GA1.2.1030079492.1319781868; _gat=1' -H 'Connection: keep-alive' --compressed
# curl 'https://avosapi.delicious.com/api/v1/posts/related/links?limit=7&md5=950a4f5dd102ccbc371cbeea1c9a7c31&_=1416161708275' -H 'Origin: https://delicious.com' -H 'Accept-Encoding: gzip,deflate' -H 'Accept-Language: es-419,es;q=0.8,ca;q=0.6,de;q=0.4,en;q=0.2,eu;q=0.2,fr;q=0.2,gl;q=0.2,pt;q=0.2,ru;q=0.2' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/38.0.2125.111 Chrome/38.0.2125.111 Safari/537.36' -H 'Accept: ' -H 'Referer: https://delicious.com/link/950a4f5dd102ccbc371cbeea1c9a7c31' -H 'Cookie: company_history=%5B%5B%22http%3A//support.delicious.com/delicious%22%2C%22Delicious%22%5D%5D; avid=1kwyiwaz2b4rdxfdwnsbzbs8l; optimizelyEndUserId=oeu1414888627893r0.4138932339847088; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%222128660043%22%3A%222087051005%22%7D; __qca=P0-390458789-1416134340213; __utma=249254418.1030079492.1319781868.1416134868.1416161047.573; __utmc=249254418; __utmz=249254418.1416161047.573.3.utmcsr=programmableweb.com|utmccn=(referral)|utmcmd=referral|utmcct=/api/del.icio.us; _ga=GA1.2.1030079492.1319781868; _gat=1' -H 'Connection: keep-alive' --compressed
# curl 'https://avosapi.delicious.com/api/v1/posts/comments/time/950a4f5dd102ccbc371cbeea1c9a7c31?limit=20&anchor=-1&exclude_yours=false&include_empty=true&_=1416161708274' -H 'Origin: https://delicious.com' -H 'Accept-Encoding: gzip,deflate' -H 'Accept-Language: es-419,es;q=0.8,ca;q=0.6,de;q=0.4,en;q=0.2,eu;q=0.2,fr;q=0.2,gl;q=0.2,pt;q=0.2,ru;q=0.2' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/38.0.2125.111 Chrome/38.0.2125.111 Safari/537.36' -H 'Accept: ' -H 'Referer: https://delicious.com/link/950a4f5dd102ccbc371cbeea1c9a7c31' -H 'Cookie: company_history=%5B%5B%22http%3A//support.delicious.com/delicious%22%2C%22Delicious%22%5D%5D; avid=1kwyiwaz2b4rdxfdwnsbzbs8l; optimizelyEndUserId=oeu1414888627893r0.4138932339847088; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%222128660043%22%3A%222087051005%22%7D; __qca=P0-390458789-1416134340213; __utma=249254418.1030079492.1319781868.1416134868.1416161047.573; __utmc=249254418; __utmz=249254418.1416161047.573.3.utmcsr=programmableweb.com|utmccn=(referral)|utmcmd=referral|utmcct=/api/del.icio.us; _ga=GA1.2.1030079492.1319781868; _gat=1' -H 'Connection: keep-alive' --compressed

# curl --data "client_id=4269302d99c97fd93d143d78bd7c4592&client_secret=e6965b38674a3bcc9223783c01d638bf&grant_type=code&code=b4d2325534966ff16094e19d5b23146a" https://avosapi.delicious.com/api/v1/oauth/token
# curl --data "client_id=4269302d99c97fd93d143d78bd7c4592&client_secret=e6965b38674a3bcc9223783c01d638bf&username=alabarga&password=tour98&grant_type=credentials" https://avosapi.delicious.com/api/v1/oauth/token
# {"pkg":null,"status":"success","url":"http://avosapi.delicious.com/api/v1/oauth/token","delta_ms":33,"server":"ip-10-196-105-143.us-west-1.compute.internal","session":"1ae2cd1zhshu1m3e2qfx4yh6t","api_mgmt_ms":0,"version":"v1","access_token":"664532-619ed0df9ba594eb9b6f5f884d3e5e13"}

class Delicious(SocialNetworkAPI):

    def __init__(self):
        
        self.base_url = 'https://avosapi.delicious.com/api/v1/posts/'
        super(Delicious, self).__init__("delicious")

    def auth(self):

        clientId = '4269302d99c97fd93d143d78bd7c4592'
        code = 'b4d2325534966ff16094e19d5b23146a'
        # https://avosapi.delicious.com/api/v1/oauth/token?client_id=f5dad5a834775d3811cdcfd6a37af312&client_secret=7363879fee6c3ab0f93efbd24111ad34&grant_type=code&code=fa746b2eb266cab06f34fb7bc3d51160


        return token

    def get_md5(self,url):

        api_url = '%s%s?url=' % (self.base_url,'compose',urllib.urlencode(url))

        response=urllib2.urlopen(api_url)        
        result =json.loads(response.read())

        md5 = result['pkg']['md5']

        # https://avosapi.delicious.com/api/v1/oauth/token?client_id=f5dad5a834775d3811cdcfd6a37af312&client_secret=7363879fee6c3ab0f93efbd24111ad34&grant_type=code&code=fa746b2eb266cab06f34fb7bc3d51160


        return md5

    def find_mentions(self,url):

        api_url = '%s%s%s' % (self.base_url,'comments/time/',self.get_md5(url))

        response=urllib2.urlopen(api_url)        
        result =json.loads(response.read())
       
        

    def get_expand(url,user,tag,social_network):
        tagl=[]
        tagl.append(str(tag))
        relatedToTweet=[]        
       
        print"----------------------------"  
        print "En delicious para el usuario "+user+" y tag "+str(tag)+": "
        url_to_call="http://feeds.delicious.com/v2/json/"+str(user)+"/"+urllib2.quote(str(tag),'') 
        response=urllib2.urlopen(url_to_call)
        response=json.loads(response.read())
        for res in response:
            if url!=str(res["u"]):
                print str(res["u"])
                print "Fecha: "+res["dt"]
                call_command('add',URL=str(res["u"]))
                feed=feedfinder.feed(str(res["u"]))
                if feed:
                    rc=ResourceContainer.objects.get_or_create(rss=feed,url=str(res["u"]))
                    add_feed(feed)
        print "__________________________"
        print ""     
