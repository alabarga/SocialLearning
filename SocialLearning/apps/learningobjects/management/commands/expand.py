#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
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
#####TWITTER KEYS#####
CONSUMER_KEY = 'ieZUZgZrSJJE0QLBBOsgXg'
CONSUMER_SECRET = 'PlIpSrh6unKYZISSDieBIFAB3D9f6aSh4p4Dmcn8Q'
OAUTH_TOKEN = '1015949947-0Akq5OBnEzTp7OwaIuvLNiKN6L52FNLVOW9yIyf'
OAUTH_TOKEN_SECRET = 'SJz3nXcyGt2lIKhmPiFg5VlTdHLbrRSPRRgUZ552xfe1e'
####Twitter auth handler####
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
twittApi = tweepy.API(auth)

class Command(BaseCommand):
    args = 'query'
    help = 'Expandir el numero de documentos'

    option_list = BaseCommand.option_list + (
        make_option('-u','--url',
            dest='URL',
            help='URL del recurso'),
        )

    def handle(self, *args, **options):
        results=[]
        if options['URL'] == None:   
            inp=raw_input("This will expand EVERY Resource with ´Described´ status on the database. Are you sure(y/n)?:")
            inp=inp.lower()
            if inp=="y" or inp=="yes":
                resources=Resource.objects.filter(status=Resource.DISCOVERED)
                for res in resources:
                    url=res.url
                    #res.status=Resource.DISCOVERED
                    res.save()
                    print "Updated.."
        else:
            url=options['URL']
            print url
            try:
                resource=Resource.objects.get(url=url,status=Resource.DISCOVERED)
            except:
                print "That link is not in the database or is not with ´Described´ status. Add it first (python manage.py add -u "+url+")"
            #para cada mencion conseguir usuario y tags y hacer:
            user="GontzalYrth"#getuser
            user2="yrthgze"
            tags=resource.tags.all()
            print "Para la url "+url+" tenemos las siguientes urls relacionadas:"
            for tag in tags:
                get_expand(url,user,tag,"twitter")
                get_expand(url,user2,tag,"delicious")
            #resource.update(status=Resource.EXPANDED)

def get_expand(url,user,tag,social_network):
    tagl=[]
    tagl.append(str(tag))
    relatedToTweet=[]        
    if social_network=="twitter":
        print "En twitter para el usuario "+user+" y tag "+str(tag)+": "
        response=twittApi.user_timeline(user=user,count=10)
        for tweet in response:
            ht=extract_hash_tags(tweet.text)           
            intersect=list(set(tagl) & set(ht))
            if len(intersect)>0:
                #relatedToTweet.append(tweet)
                ##mirar si en el texto hay enlaces
                ##para cada enlace dle texto
                links= extract_urls(str(tweet.text))
                for link in links:
                    link=resolve(link)
                    if link!=url:
                        print link
                        print "Fecha: "+str(tweet.created_at)
        print ""
        """for link in links:
                    Resource=self.createResource(link,firsturl,1)
                    try:
                        resources.insert(Resource)
                        print "Succesfully inserted related resource twitter"
                    except:
                        print "Something went wrong you silly boy in related twitter"""
    elif social_network=="delicious":    
        print "En delicious para el usuario "+user+" y tag "+str(tag)+": "
        firsturl=url
        url="http://feeds.delicious.com/v2/json/"+str(user)+"/"+urllib2.quote(str(tag),'') 
        response=urllib2.urlopen(url)
        resp=json.loads(response.read())
        for res in resp:
            if firsturl!=str(res["u"]):
                print str(res["u"])
                print "Fecha: "+res["dt"]
        print ""
                
    else:
        print "Este enlace no tiene nada de twitter ni deli"
        

def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))

def extract_urls(s):
    a= re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)
    return a