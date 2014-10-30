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
        make_option('-u','--url',
            dest='URL',
            help='URL del recurso'),
        )

    def handle(self, *args, **options):
    	results=[]
    	if options['query'] == None:

    		#r = Resource.objects.filter(status=Resource.ADDED)
    		#for res in r:
			#	results+=r.url				
            raise CommandError("Option `--query=...` must be specified.")
        else:
			
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
		for l in results:
			r=createResource(l)
			m=createMention(l,r)
        #a=Resource.objects.all()
        #print "Recursos en la base de datos"
        #print a

def createResource(url):
	if resolve(url)!=None:
		url=resolve(url)
	g = Goose()
	a= g.extract(url=url)
	r=Resource.objects.filter(url=url)
	if len(r)>0:		
		print "El recurso ya lo tenia"
		r=r[0]
	else:
		if a.title==None or a.title=="":
			title="notitle"
		else:
			title=a.title
		r=Resource.objects.create(title=title,url=url,category="post")
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
			print "Creado el usuario "+s
			Mention.objects.create(profile=s,resource=res)
			print "Creada mention para delicious"
	for r in twitRes:
		author=r.author.name
		s=SocialProfile.objects.filter(username=author)
		if len(s)==0:
			user_url="https://twitter.com/"+author
			sn=SocialNetwork.objects.create(name="Twitter",url="http://twitter.com/")
			s=SocialProfile.objects.create(username=author,social_network=sn,url=user_url)
			print "Creado el usuario "+str(s)
			Mention.objects.create(profile=s,resource=res)
			print "Creada mention para twitter"
	  
