#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option


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
            inp=raw_input("This will expand EVERY Resource with ´Described´ status on the database. Are you sure(y/n)?:")
            inp=inp.lower()
            if inp=="y" or inp=="yes":
                resources=Resource.objects.filter(status=Resource.DISCOVERED)
                for res in resources:
                    url=res.url
                    res.status=Resource.DISCOVERED
                    res.save()
                    print "Updated.."
        else:
            url=options['URL']
            resource=Resource.objects.filter(url=url,status=Resource.DISCOVERED)
            if len(resource)>0:
                
                resource.update(status=Resource.EXPANDED)
            else:
                print "That link is not in the database or is not with ´Discovered´ status. Add it first (python manage.py add -u "+url+")"
