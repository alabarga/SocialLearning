enlaces_iniciales = ['http://www.edutopia.org/project-based-learning-history',
'http://bie.org/about/why_pbl',
'http://es.wikipedia.org/wiki/Aprendizaje_basado_en_proyectos',
'http://en.wikipedia.org/wiki/Project-based_learning',
'https://www.youtube.com/watch?v=LMCZvGesRz8',
'http://www.learnnc.org/lp/pages/4753',
'http://www.ascd.org/publications/educational_leadership/sept10/vol68/num01/seven_essentials_for_project-based_learning.aspx',
'http://eric.ed.gov/?q=%22%22&ff1=subActive+Learning',
'http://eric.ed.gov/?q=%22%22&ff1=subStudent+Projects']

from learningobjects.utils.alchemyapi import AlchemyAPI
from learningobjects.utils.parsers import *
from learningobjects.utils.search import *
from ftfy import fix_text
import urllib

url = enlaces_iniciales[0]

texto = ''
tags = set()

for url in enlaces_iniciales:
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
    more_links.add(res)

google = Google()
for res in google.search('related:'+url):
    more_links.add(res)
    if len(more_links) > 30:
        break

duck = DuckDuckGo()
for link in enlaces_iniciales:
    for res in duck.search_related(link):
        more_links.add(res)


"""
response = alchemyapi.entities("text", texto)
if response['status'] == 'OK':
    noticia.entities = response["entities"]
else:
    print response['statusInfo']

"""