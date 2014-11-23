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

