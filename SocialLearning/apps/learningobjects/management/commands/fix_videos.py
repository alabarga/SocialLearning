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
from learningobjects.utils import youtube

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

        
        resources=Resource.objects.all()
        for res in resources:

            try:
                url = res.url
                res.identifier = hashlib.md5(url).hexdigest()
                if options['log']: print url
                u = URLObject(url)
                if options['log']: print u.content_type
                if bool(re.match('^(http(s|):\/\/|)(www.|)youtube.com',u.url)):
                    yt_desc = YoutubeParser(url).describe()
                    res.title = yt_desc.title
                    res.description = yt_desc.description
                    res.interest = yt_desc.viewcount
                else:
                    continue
                
                res.save()

                rc_url = 'https://www.youtube.com/user/' + yt_desc.username
                rc_rss = 'http://gdata.youtube.com/feeds/api/users/' + yt_desc.username + '/uploads'
                rc = ResourceContainer.objects.get_or_create(url=rc_url, rss=rc_rss, name=yt_desc.username )
                
                rc.resources.add(res)
                
                            

            except:
                continue

