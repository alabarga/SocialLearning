#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
from learningobjects.utils.search import *
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import urllib2
import hashlib
import json

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
            inp=raw_input("This will discover EVERY Resource with ´Described´ status on the database. Are you sure(y/n)?:")
            inp=inp.lower()
            if inp=="y" or inp=="yes":
                resources=Resource.objects.filter(status=Resource.DESCRIBED)
                for res in resources:
                    url=res.url
                    res.status=Resource.DISCOVERED
                    tags=getTags(url)
                    for tag in tags:
                        res.tags.add(tag)
                    print res.tags.all()
                    res.save()
                    print "Updated.."
        else:
            url=options['URL']
            try:
                resource=Resource.objects.get(url=url,status=Resource.DESCRIBED)
            except:
                print "That link is not in the database or is not with ´Described´ status. Add it first (python manage.py add -u "+url+")"            
            tags=getTags(url)
            for tag in tags:
                resource.tags.add(tag)
            print resource.tags.all()
            resource.status=Resource.DISCOVERED
            resource.save()
            
            
def getTags(url):
    furl=url
    engine=SearchEngine("none")
    url=engine.clean(url)
    url=hashlib.md5(url).hexdigest()
    response=urllib2.urlopen("http://feeds.delicious.com/v2/json/url/"+url)        
    delRes=json.loads(response.read())
    delRes=[]#delicious sigue sin funcionar
    s=twittApi
    twitRes=s.search(furl)
    tags=[]
    for a in delRes:
        for t in a["t"]:
            if t not in tags:
                tags.insert(0,t)
    for r in twitRes:
        hts=extract_hash_tags(r.text)
        for ht in hts:
            if ht not in tags:
                tags.insert(0,ht)
    return tags

def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))