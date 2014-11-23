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

        if options['URL'] == None:   
            inp=raw_input("This will describe EVERY Resource with ´Added´ status on the database. Are you sure(y/n)?:")
            inp=inp.lower()
            if inp=="y" or inp=="yes":
                resources=Resource.objects.filter(status=Resource.ADDED)
                for res in resources:
                    url=res.url
                    res.identifier = 
                    rp_desc = ReadibilityParser.describe(url)

                    res.title = data.title
                    res.description = data.excerpt
                    # res.author =                    
                    res.status=Resource.DESCRIBED
                    res.save()

        else:
            url=options['URL']
            resource=Resource.objects.filter(url=url,status=Resource.ADDED)
            if len(resource)>0:

                data = ReadibilityParser.describe(url)               
                resource.update(status=Resource.DESCRIBED)
            else:
                print "That link is not in the database or is not with ´Added´ status. Add it first (python manage.py add -u "+url+")"
