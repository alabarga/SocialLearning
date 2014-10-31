from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
from goose import Goose
from urlunshort import resolve
import hashlib


class Command(BaseCommand):
    args = 'query'
    help = 'Expandir el numero de documentos'

    option_list = BaseCommand.option_list + (
        make_option('-q','--query',
            dest='query',
            help='Palabra clave a buscar'),
        )+(
        make_option('-u','--url',
            dest='URL',
            help='URL del recurso'),
        )

    def handle(self, *args, **options):
        results=[]
        if options['query'] == None and options['URL'] == None:
            raise CommandError("Option `--query=...` or `--url=...` must be specified.")
        elif options['query'] != None:
            query=options['query']
            print "You searched for "+query
            d=DuckDuckGoIO()
            s=Slideshare()
            engines=[d,s]
            for engine in engines:
                links=engine.search(query)
                #for index in range(len(links)):
                #    links[index]=engine.clean(links[index])
                results+=links
        else:
            url=options['URL']
            print "You want to add: "+url
            results=[url]
        for l in results:
            r=createResource(l)

def createResource(url):
    if len(url)>200:
        print "Los links largos de duckduckgo no funcionan"
        return None
    else:
        r=Resource.objects.filter(url=url)
        if len(r)>0:        
            print "El recurso ya lo tenia"
            r=r[0]
        else:
            g = Goose()
            a= g.extract(url=url)   
            if a.title==None or a.title=="":
                title="notitle"
            else:
                title=a.title
            try:
                r=Resource.objects.create(title=title,url=url,status=Resource.ADDED)
            except:
                print "no ha ido bien"
                print title
                print url
            print "Creado el recurso para "+url
        return r            