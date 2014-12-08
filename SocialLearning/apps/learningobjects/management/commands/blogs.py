#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
from learningobjects.utils import feedfinder
from learningobjects.management.commands import add
from django.core.management import call_command
import feedparser

from learningobjects.utils.parsers import *
from learningobjects.utils.alchemyapi import AlchemyAPI
from learningobjects.utils import slideshare
import feedparser

class Command(BaseCommand):
    args = 'query'
    help = 'Expandir el numero de documentos'
    """make_option('-v','--verbose',
            dest='verbose',
            help='verbose'),"""

#    option_list = BaseCommand.option_list + (
#        make_option('-u','--url',
#            dest='URL',
#            help='URL del recurso'),      
#        ) 

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u','--url',
            dest='URL',
            help='URL del recurso'), )

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
                
        #topics = Topic.objects.all()
        #resources=Resource.objects.filter(status=Resource.ADDED)
        #slides = slideshare.SlideshareAPI()
        
        containers=ResourceContainer.objects.all()
        for cont in containers:
            feed = cont.rss
            feed_res = feedparser.parse(feed)
            for e in feed_res['entries']:
                url = e['link']
                u = URLObject(url)
                h = hashlib.md5(url).hexdigest()
                res, created = Resource.objects.get_or_create(identifier=h, url=url)
                print url
                if created:
                    res.url = url
                    res.title = e['title']
                    res.description = e['description']
                    res.save()

