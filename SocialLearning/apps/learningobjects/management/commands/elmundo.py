#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
from learningobjects.utils import feedfinder
from learningobjects.management.commands import add
from django.core.management import call_command
import feedparser
import hashlib
import random
import requests

from learningobjects.utils.parsers import *
from learningobjects.utils.alchemyapi import AlchemyAPI

import feedparser
from bs4 import BeautifulSoup

from time import mktime
from datetime import datetime, date
from dateutil import parser

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


def feed_modified_date(feed):
    # this is the last-modified value in the response header
    # do not confuse this with the time that is in each feed as the server
    # may be using a different timezone for last-resposne headers than it 
    # uses for the publish date

    modified = feed.get('modified')
    if modified is not None:
        return modified

    return None

def max_entry_date(feed):
    entry_pub_dates = (e.get('published_parsed') for e in feed.entries)
    entry_pub_dates = tuple(e for e in entry_pub_dates if e is not None)

    if len(entry_pub_dates) > 0:
        return max(entry_pub_dates)    

    return None

def entries_with_dates_after(feed, date):
    response = []

    for entry in feed.entries:
        if entry.get('published_parsed') > date:
            response.append(entry)

    return response            

def defaultJson(o):
    if type(o) is date or type(o) is datetime:
        return o.isoformat()

class Command(BaseCommand):

    help = 'Describe los documentos'

    option_list = BaseCommand.option_list + (
        make_option('--url',
            dest='URL',
            default=False,
            help='URL'),
        make_option('--log',
            action='store_true',
            dest='log',
            default=False,
            help='log info'),
        )

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u','--url',
            nargs=1,
            dest='URL',
            help='URL del recurso')

        #parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument('--log',
            nargs=0,
            action='store_true',
            dest='log',
            default=False,
            help='Log actions to console')


    def handle(self, *args, **options):

        rsslist=["http://www.elmundo.es/rss/hackathon/espana.xml", "http://www.elmundo.es/rss/hackathon/internacional.xml"]

        from pymongo import MongoClient
        client = MongoClient('mongodb://grserrano.net:27017/')
        from pymongo import Connection
        connection = Connection()
        db = connection['elmundo']
        collection = db['test-noticias']
        alchemyapi = AlchemyAPI()

        noticias = []
        for feed_url in rsslist:
            print('--------%s-------' % feed_url)
            d = feedparser.parse(feed_url)
            print('feed length %i' % len(d.entries))

            for entry in d.entries:
                print entry.title
                print "%s - %s" % (entry.author,entry.published)
                print entry.link

                resumen =  BeautifulSoup(entry.summary).get_text()
               
                texto =  BeautifulSoup(entry.summary).get_text()

                noticia = dotdict()

                noticia.titulo = entry.title
                noticia.resumen = resumen
                noticia.texto = texto
                noticia.enlace = entry.link

                if entry.has_key('media_content'):
                    noticia.media = entry.media_content[0]['url']
                    print entry.media_content[0]['url']

                noticia.fecha = parser.parse(entry.published)

                if entry.has_key('tags'):
                    noticia.tags = entry.tags
                    print ', '.join([tag.term for tag in entry.tags])

                response = alchemyapi.sentiment("text", texto)
                if response['status'] == 'OK':
                    noticia.sentiment = response["docSentiment"]
                else:
                    print response['statusInfo']            

                response = alchemyapi.entities("text", texto)
                if response['status'] == 'OK':
                    noticia.entities = response["entities"]
                else:
                    print response['statusInfo']
                
                noticias.append(noticia)
                collection.insert(noticia)

        with open('noticias.json', 'w') as outfile:
            json.dump(noticias, outfile, default=defaultJson)

            """
            import datetime
            post = {"author": "Mike",
                    "text": "My first blog post!",
                    "tags": ["mongodb", "python", "pymongo"],
                    "date": datetime.datetime.utcnow()}

            collection.insert(post)
            """


            #rr = Resource.objects.all()
            #rs = ResourceMongoSerializer()
            #rs.to_native(rr[0])


            """
            import json
            from django.core import serializers

            def getObject(request, id):
                obj = MyModel.objects.get(pk=id)
                data = serializers.serialize('json', [obj,])

            """
            """
            ['summary_detail',
            'published_parsed',
            'media_description',
            'links',
            'author',
            'title',
            'media_thumbnail',
            'summary',
            'guidislink',
            'title_detail',
            'href',
            'link',
            'authors',
            'author_detail',
            'media_content',
            'id',
            'tags',
            'published']

            """

            """
            if len(d.entries) > 0:
                etag = d.feed.get('etag', None)
                modified = feed_modified_date(d)
                print('modified at %s' % modified)

                d2 = feedparser.parse(feed_url, etag=etag, modified=modified)
                print('second feed length %i' % len(d2.entries))
                if len(d2.entries) > 0:
                    print("server does not support etags or there are new entries")
                    # perhaps the server does not support etags or last-modified
                    # filter entries ourself

                    prev_max_date = max_entry_date(d)

                    entries = entries_with_dates_after(d2, prev_max_date)

                    print('%i new entries' % len(entries))
                else:
                    print('there are no entries')

                """

"""   
topics = Topic.objects.all()
resources=Resource.objects.filter(status=Resource.ADDED)
for res in resources:

    try:
        url = res.url
        res.identifier = hashlib.md5(url).hexdigest()
        if options['log']: print url
        u = URLObject(url)
        if options['log']: print u.content_type
        if 'application/pdf' in u.content_type:
            pd = PDFParser(url).describe()
            res.fulltext = pd.fulltext
        elif 'text/html'  in u.content_type:
            
            rp_desc = ReadibilityParser(url).describe()
            gp_desc = GooseParser(url).describe()
            sm_desc = SummaryParser(url).describe()

            res.title = rp_desc.title
            res.description = rp_desc.cleaned_text
            res.fulltext = gp_desc.fulltext

            # res.author = 
            if options['log']: print rp_desc.author
            if options['log']: print rp_desc.title
            if options['log']: print rp_desc.excerpt
        else:
            continue

        for t in topics:
            rel, created =  Relevance.objects.get_or_create(resource=res, topic=t)
            rel.score = random.random()
               
        res.status=Resource.DESCRIBED
        res.save()

    except:
        continue

"""