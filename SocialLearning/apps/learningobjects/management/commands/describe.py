#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
from learningobjects.utils import feedfinder
from learningobjects.management.commands import add
from django.core.management import call_command
import feedparser

from learningobjects.utils.parsers import ReadibilityParser
from learningobjects.utils.alchemyapi import AlchemyAPI
from learningobjects.utils import slideshare
from textblob import TextBlob
# pip install -U textblob
# python -m textblob.download_corpora

class Command(BaseCommand):
 
    option_list = BaseCommand.option_list + (
        make_option('-q','--query',
            dest='query',
            help='Palabra clave a buscar'),
        )+(
        make_option('-u','--url',
            dest='URL',
            help='URL del recurso'),
        )

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u','--url',
            dest='URL',
            help='URL del recurso')

        #parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Log actions to console')

    def handle(self, *args, **options):
        results=[]

        alchemyapi = AlchemyAPI()

        if options['URL'] == None:   
            inp=raw_input("This will describe EVERY Resource with ´Added´ status on the database. Are you sure(y/n)?:")
            inp=inp.lower()
            if inp=="y" or inp=="yes":
                
                topics = Topic.objects.all()
                #resources=Resource.objects.filter(status=Resource.ADDED)

                col = Collection.objects.get(pk=23)
                resources = col.resources.all()

                slides = slideshare.SlideshareAPI()

                for res in resources:

                    try:
                        url = res.url
                        print url
                        res.identifier = hashlib.md5(url).hexdigest()
                        u = URLObject(url)
                        print u.content_type
                        if 'application/pdf' in u.content_type:
                            pd = PDFParser(url).describe()
                            res.fulltext = pd.fulltext
                            res.content_type = 'PDF'

                        # slideshare
                        elif bool(re.match('^(http(s|):\/\/|)(www.|)slideshare.net',u.url)):
                            s = slides.get_slideshow(slideshow_url=u.url)
                            res.title = slide['Slideshow']['Title']
                            res.description = slide['Slideshow']['Description']
                            res.author = slide['Slideshow']['Username']
                            res.fulltext = slide['Slideshow']['Embed']
                            res.interest = int(slide['Slideshow']['NumViews']) + int(slide['Slideshow']['NumFavorites']) + int(slide['Slideshow']['NumDownloads'])

                            rc_url = 'https://www.slideshare.net/' + slide['Slideshow']['Username'] + '/presentations'
                            rc_rss = 'http://es.slideshare.net/rss/user/' + slide['Slideshow']['Username']
                            rc, created = ResourceContainer.objects.get_or_create(url=rc_url, rss=rc_rss, name=slide['Slideshow']['Username'] )
                        
                            rc.resources.add(res)

                        # youtube
                        elif bool(re.match('^(http(s|):\/\/|)(www.|)youtube.com',u.url)):
                            yt_desc = YoutubeParser(url).describe()
                            res.title = yt_desc.title
                            res.description = yt_desc.description
                            res.interest = yt_desc.viewcount
                            res.content_type = 'VIDEO'

                            res.author = yt_desc.username

                            rc_url = 'https://www.youtube.com/user/' + yt_desc.username
                            rc_rss = 'http://gdata.youtube.com/feeds/api/users/' + yt_desc.username + '/uploads'
                            rc = ResourceContainer.objects.get_or_create(url=rc_url, rss=rc_rss, name=yt_desc.username )
                        
                            rc.resources.add(res)

                        elif 'text/html'  in u.content_type:
                            
                            rp_desc = ReadibilityParser(url).describe()
                            gp_desc = GooseParser(url).describe()
                            sm_desc = SummaryParser(url).describe()

                            res.title = rp_desc.title
                            res.description = rp_desc.cleaned_text
                            res.fulltext = gp_desc.fulltext
                            np = TextBlob(rp_desc.cleaned_text)
                            res.language = np.detect_language()
                            res.author = rp_desc.author
                            res.content_type = 'WEB'

                        else:
                            continue

                        #for t in topics:
                        #    rel, created =  Relevance.objects.get_or_create(resource=res, topic=t)
                        #    rel.score = random.random()
                               
                        res.status=Resource.DESCRIBED
                        res.save()

                        
                        
                        

                    except:
                        continue

        else:


            url=options['URL']
            resource=Resource.objects.filter(url=url,status=Resource.ADDED)
            if len(resource)>0:

                data = ReadibilityParser.describe(url)               
                resource.update(status=Resource.DESCRIBED)
            else:
                print "That link is not in the database or is not with ´Added´ status. Add it first (python manage.py add -u "+url+")"
