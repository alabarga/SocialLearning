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
                for resource in resources:
                    url=resource.url
                    resource.status=Resource.DISCOVERED
                    author, tags=getMentions(url,resource)
                    for tag in tags:
                        resource.tags.add(tag)
                    #print resource.tags.all()
                    resource.save()
                    #print "Updated.."
        else:
            url=options['URL']
            try:
                resource=Resource.objects.get(url=url,status=Resource.DESCRIBED)
            except:
                print "That link is not in the database or is not with ´Described´ status. Add it first (python manage.py add -u "+url+")"            
            author,tags=getMentions(url,resource)
            for tag in tags:
                resource.tags.add(tag)
            #print resource.tags.all()
            resource.status=Resource.DISCOVERED
            resource.save()

            
            
def getMentions(url,resource):
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
    authors=[]
    #print "--------------Menciones-------------------------"
    #print "La url "+furl+" tiene las siguiente menciones:"
    for a in delRes:
        author=a["a"]
        if author not in authors:
            authors.insert(0,author)
        for t in a["t"]:
            if t not in tags:
                tags.insert(0,t)
    for r in twitRes:
        author=r.user.screen_name
        user_url="https://twitter.com/"+author
        if author not in authors:
            authors.insert(0,author)
        hts=extract_hash_tags(r.text)
        inner_t=[]
        for ht in hts:
            if ht not in tags:
                tags.insert(0,ht)
            inner_t.append(ht)
        #print "En Twitter, Usuario: "+author+", Tags: "+", ".join(inner_t)+", Fecha: "+str(r.created_at)
        sn=SocialNetwork.objects.get_or_create(name="Twitter",url="http://twitter.com")[0]
        sp=SocialProfile.objects.get_or_create(username=author,social_network=sn,url="http://twitter.com/"+str(author))
        m=Mention.objects.get_or_create(profile=sp[0],resource=resource)[0]
        m.tags.add("")
    return authors, tags

def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))
"""
def createInstance(model,**kwargs):
    if model=="SocialNetwork":
        sn=SocialNetwork.objects.filter(name=kwargs["name"])
        if len(sn)==0:
            sn=SocialNetwork.objects.create(name=kwargs["name"],url=kwargs["url"])
        else:
            sn=sn[0]
        return sn
    if model=="SocialProfile":
        sp=SocialProfile.objects.filter(username=kwargs["username"],social_network=kwargs["sn"])
        if len(sp)==0:
            sp=SocialProfile.objects.create(username=kwargs["username"],social_network=kwargs["sn"],url=kwargs["user_url"])
        else:
            sp=sp[0]
        return sp
    if model=="Mention":
        m=Mention.objects.filter(profile=kwargs["sp"],resource=kwargs["resource"])
        if len(m)==0:
            m=Mention.objects.create(profile=kwargs["sp"],resource=kwargs["resource"])
            m.tags.add("")
            print "mencion creada"
        else:
            m=m[0]
            print "Esa mencion ya estaba"
        return m"""