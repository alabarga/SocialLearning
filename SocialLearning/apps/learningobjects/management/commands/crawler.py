from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
from goose import Goose
from urlunshort import resolve
import hashlib
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from random import shuffle
import re

#####TWITTER KEYS#####
CONSUMER_KEY = 'ieZUZgZrSJJE0QLBBOsgXg'
CONSUMER_SECRET = 'PlIpSrh6unKYZISSDieBIFAB3D9f6aSh4p4Dmcn8Q'
OAUTH_TOKEN = '1015949947-0Akq5OBnEzTp7OwaIuvLNiKN6L52FNLVOW9yIyf'
OAUTH_TOKEN_SECRET = 'SJz3nXcyGt2lIKhmPiFg5VlTdHLbrRSPRRgUZ552xfe1e'
###Twitter auth handler####
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
twittApi = tweepy.API(auth)

class Command(BaseCommand):
    args = 'query'
    help = 'Expandir el numero de documentos'

    option_list = BaseCommand.option_list + (
        make_option('-q','--query',
            dest='query',
            help='Palabra clave a buscar'),
        )

    def handle(self, *args, **options):
    	if options['query'] == None:
            raise CommandError("Option `--query=...` must be specified.")
        else:
			results=[]
			query=options['query']
			print "You searched for "+query
            #no funciong=Google()
			d=DuckDuckGoIO()
			s=Slideshare()
			engines=[d,s]
			for engine in engines:
				links=engine.search(query)
				#for index in range(len(links)):
				#  links[index]=engine.clean(links[index]) el unfurl aveces no funciona
				results+=links
			shuffle(results)
			results=results[:15]
			#results=['http://mashable.com/category/3d-printing/']
			for l in results:
				r=createResource(l)
				if r!=None:
					m=createMention(l,r)


def createResource(url):
	if resolve(url)!=None:
		url=resolve(url)
	g = Goose()
	a= g.extract(url=url)
	if len(url)>200:
		print "Los links largos de duckduckgo no funcionan"
		return None
	else:
		r=Resource.objects.filter(url=url)
		if len(r)>0:		
			print "El recurso ya lo tenia"
			r=r[0]
		else:
			if a.title==None or a.title=="":
				title="notitle"
			else:
				title=a.title
			try:
				r=Resource.objects.create(title=title,url=url,category="post")
			except:
				print "no ha ido bien"
				print title
				print url
			print "Creado el recurso para "+url
		return r

def createMention(url,res):
	if resolve(url)!=None:
		furl=resolve(url)
	else:
		furl=url
	url=hashlib.md5(furl).hexdigest()
	response=urllib2.urlopen("http://feeds.delicious.com/v2/json/url/"+url)        
	delRes=json.loads(response.read())
	delRes=[]#EL RSS DE DELICIOUS NO ESTA FUNCIONANDO PARA LAS URL, EL DE USUARIOS SIGUE ACTIVO
	s=twittApi
	twitRes=s.search(furl)
	for a in delRes:
		print a
		author=a["a"]
		s=SocialProfile.objects.filter(username=author)
		if len(s)==0:
			user_url="https://delicious.com/"+author
			s=SocialProfile.objects.create(username=author,social_network="Delicious",url=user_url)
			print "Creado el usuario "+str(s)
			Mention.objects.create(profile=s,resource=res)
			print "Creada mention para delicious"
		##Get tags
	for r in twitRes:
		author=r.user.screen_name
		s=SocialProfile.objects.filter(username=author)
		if len(s)==0:
			user_url="https://twitter.com/"+author
			sn=SocialNetwork.objects.create(name="Twitter",url="http://twitter.com/")
			s=SocialProfile.objects.create(username=author,social_network=sn,url=user_url)
			print "Creado el usuario "+str(s)
			Mention.objects.create(profile=s,resource=res)
			print "Creada mention para twitter"
	  	##Get tags
		hts=extract_hash_tags(r.text)
		for ht in hts:
			rt=relatedTo(author,furl,ht,"twitter",r.id)
			print "____________"
			print "La url "+furl+" esta relacionada con:"
			print ""
			print rt 
			print "------------"


def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))      

def extract_urls(s):
    a= re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)
    return a

def relatedTo(user,url,tag,social_network,max_id=0):
    firsturl=url
    tagl=[]
    tagl.append(tag)
    relatedToTweet=[]
    relatedToDel=[]
    results=[]
    if social_network=="twitter":
        print "Entrado en reltated totwitter para: "+url
        response=twittApi.user_timeline(user=user,count=50)
        for tweet in response:
            ht=extract_hash_tags(tweet.text)
            intersect=list(set(tagl) & set(ht))
            if len(intersect)>0:
                #relatedToTweet.append(tweet)
                ##mirar si en el texto hay enlaces
                ##para cada enlace dle texto
                links= extract_urls(str(tweet.text))
                for link in links:
                    if resolve(link)!=None:
						link=resolve(link)
                    q=Resource.objects.filter(url=link)
                    if  len(q)==0:
                        results.append(link)
    
    elif social_network=="delicious":    
        url="http://feeds.delicious.com/v2/json/"+str(user)+"/"+urllib2.quote(str(tag),'')
        print "accediendo a"+ url#para cambiar los espacios a %20 
        response=urllib2.urlopen(url)
        print "opene2"
        resp=json.loads(response.read())
        print "opene2"
        for res in resp:
            if firsturl!=str(res["u"]):
                print "Link relacionado en delicious: "+str(res["u"])
                
                try:
                    print "Succesfully inserted resource delicious"
                except:
                    print "Something went wrong you silly boy in  delicious"
                    pass
            else:
                print "eran el mimso url"

    return results