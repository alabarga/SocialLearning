#-*- coding: UTF-8 -*-
from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
import readability
import xlsxwriter
from goose import Goose
from learningobjects.utils import feedfinder
import add
from django.core.management import call_command
import feedparser
from pyteaser import SummarizeUrl

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
        row=0
        workbook = xlsxwriter.Workbook('data.xlsx')
        worksheet = workbook.add_worksheet()
        if options['URL'] == None:   
            inp=raw_input("This will describe EVERY Resource with ´Added´ status on the database. Are you sure(y/n)?:")
            inp=inp.lower()
            if inp=="y" or inp=="yes":
                resources=Resource.objects.filter(status=Resource.ADDED)
                for res in resources:
                    url=res.url
                    get_def(url,worksheet,row)
                    row+=1
                    res.status=Resource.DESCRIBED
                    res.save()
                    print "Updated.."
        else:
            url=options['URL']
            resource=Resource.objects.filter(url=url,status=Resource.ADDED)
            if len(resource)>0:
                get_def(url,worksheet,row)
                row+=1
                resource.update(status=Resource.DESCRIBED)
            else:
                print "That link is not in the database or is not with ´Added´ status. Add it first (python manage.py add -u "+url+")"
        workbook.close()

def get_def(url,worksheet,r):
    row = r*18
    col = 0
    try:
        response=red_par.get_article_content(url.encode('utf-8')).content
    except:
        response=None
    g = Goose()
    try:
        a= g.extract(url=url.encode('utf-8'))  
    except:
        a=None
    summaries=SummarizeUrl(url.encode('utf-8'))
    print summaries
    response=getAtrib(response)
    data=[]
    #['tags',a.tags],
    keys=['domain','author','url_hash','url','meta_keywords','meta_lang','meta_description','short_url','title','excerpt','date_published','publish_date']
    for key in keys:
        if response!=None and key in response and response[key]!=None and len(response[key])>0:
            rowData=[key,response[key]]
        elif a!=None and key in dir(a) and getattr(a,key)!=None and len(getattr(a,key))>0:
            rowData=[key,getattr(a,key)]
        else:
            rowData=[key,""]
        data.append(rowData)
    feeds=feedfinder.feeds(url+"feed")
    i=0
    for f in feeds:
        data.append(["feed"+str(i),f])
    worksheet.write(row, col,"Described for url: "+url)
    row+=1
    # Iterate over the data and write it out row by row.
    for item, d in (data):
        worksheet.write(row, col,item)
        worksheet.write(row, col + 1, d)
        row += 1
    worksheet.write(row, col,"  ")
    add_feed(feeds)

def add_feed(feeds):
    for feed in feeds:
        res=Resource.objects.filter(url=feed)
        if len(res)==0:
            r=feedparser.parse(feed)
            i=0
            for entry in r.entries:
                link=entry.links[0].href
                call_command('add', 'foo', URL=str(link))
                if i<5:
                    i+=1
                else:
                    break

def getAtrib(res):
    keys=['domain','author','url','short_url','title','excerpt','date_published']
    for key in keys:
        if key not in res.viewkeys():
            res[key]=""
    return res
