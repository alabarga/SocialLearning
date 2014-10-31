#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
import readability

###Readability parser
red_par=readability.ParserClient('03b5d5676456982e868cf57e5b6757f198ef479d')

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
            inp=raw_input("This will describe EVERY Resource with ´Added´ status on the database. Are you sure(y/n)?:")
            inp=inp.lower()
            if inp=="y" or inp=="yes":
                resources=Resource.objects.filter(status=Resource.ADDED)
                for res in resources:
                    url=res.url
                    #response=red_par.get_article_content(url).content
                    res.status=Resource.DESCRIBED
                    res.save()
                    print "Updated.."
        else:
            url=options['URL']
            resource=Resource.objects.filter(url=url,status=Resource.ADDED)
            if len(resource)>0:
                response=red_par.get_article_content(url).content
                resource.update(status=Resource.DESCRIBED)
            else:
                print "That link is not in the database or is not with ´Added´ status. Add it first (python manage.py add -u "+url+")"
