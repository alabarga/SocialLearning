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


from learningobjects.utils.interest import Interest
from learningobjects.utils.parsers import *

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

        resources=Resource.objects.filter(status=Resource.ADDED)
        for res in resources:
            print res.url
            try:
                i = Interest(res.url)
                interes = i.get_interest()

                if ((interes == 0) and (bool(re.match('^(http(s|):\/\/|)(www.|)youtube.com',u.url)))):
                    yt_desc = YoutubeParser(url).describe()
                    interes = yt_desc.viewcount / 10                
                       
                print res.url, interes
                res.interest=interes
                res.save()

            except:
                continue

