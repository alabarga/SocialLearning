from learningobjects.utils.search import *
from django.core.management.base import BaseCommand, CommandError
from learningobjects.models import *
from optparse import make_option
from goose import Goose
from urlunshort import resolve
import hashlib
import sys

from learningobjects.utils.alchemyapi import AlchemyAPI
from learningobjects.utils.parsers import *
from ftfy import fix_text
import urllib
import requests

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        for collection in Collection.objects.filter(status=Collection.ADDED):

            print collection.name
            enlaces_iniciales = set()
            texto = ''
            tags = set()
            for resource in collection.resources.all():
                url = resource.url
                enlaces_iniciales.add(url)
                gp_desc = GooseParser(url).describe()
                texto += gp_desc.text
                for tag in gp_desc.tags:
                    tags.add(tag.strip())

            texto = fix_text(texto)

            more_links = set()

            alchemyapi = AlchemyAPI()
            response = alchemyapi.keywords("text", texto)
            concept = response['keywords'][0]['text']   

            wiki = Wikipedia()
            for res in wiki.search(concept):
                print res
                more_links.add(res)

            """
            google = Google()
            for res in google.search('related:'+url):
                more_links.add(res)
                if len(more_links) > 30:
                    break
            """

            duck = DuckDuckGoIO()
            for link in enlaces_iniciales:
                for res in duck.related(link):
                    more_links.add(res)

            for link in more_links:
                identifier = hashlib.md5(url).hexdigest()
                print '%s : %s' % (identifier, link)
                res, created = Resource.objects.get_or_create(identifier=identifier, url=url)
                res.save()
                collection.resources.add(res)

        print "Added!"
