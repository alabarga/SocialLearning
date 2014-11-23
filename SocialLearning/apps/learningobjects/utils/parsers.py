from __future__ import unicode_literals
from ftfy import fix_text

import readability
from goose import Goose
from pyteaser import SummarizeUrl
import requests

from learningobjects.utils.pdf import extract_pdf



###Readability parser

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


class URLObject(object):

    @property
    def available_fields():
        return self.descriptor.viewkeys()

    @property
    def headers(self):
        r = requests.head(self.url)
        return r.headers

    @property
    def content_type(self):
        return self.headers['content-type']

    def __init__(self, url=None):
        if url != None:
            self.url = url
            self.descriptor = dotdict({'url':url})

class ReadibilityParser(URLObject):

    parser = readability.ParserClient('03b5d5676456982e868cf57e5b6757f198ef479d')

    def describe(self, url=None):

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        # Readability
        """
        [u'content',
         u'domain',
         u'author',
         u'url',
         u'short_url',
         u'title',
         u'excerpt',
         u'direction',
         u'word_count',
         u'total_pages',
         u'next_page_id',
         u'dek',
         u'lead_image_url',
         u'rendered_pages',
         u'date_published']
        """

        try:
            response=self.parser.get_article_content(url.encode('utf-8'))
            a = dotdict(response.content)
            self.descriptor.update(a)
        except:
            pass

        return self.descriptor

class GooseParser(URLObject):

    def describe(self, url=None):

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        #Goose
        """
        goose.article.Article()

         'additional_data',
         'canonical_link',
         'cleaned_text',
         'doc',
         'domain',
         'final_url',
         'link_hash',
         'meta_description',
         'meta_favicon',
         'meta_keywords',
         'meta_lang',
         'movies',
         'publish_date',
         'raw_doc',
         'raw_html',
         'tags',
         'title',
         'top_image',
         'top_node']

        """

        g = Goose()
        try:
            a = g.extract(url=url.encode('utf-8'))  
            self.descriptor.update(a)
        except:
            pass

        return self.descriptor


class SummaryParser(URLObject):

    def describe(self, url=None):        

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        summaries=SummarizeUrl(url.encode('utf-8'))

        resumen = u''
        if not(summaries is None):
            for s in summaries:
                print s
                resumen += fix_text(s.decode('utf-8'))

        self.descriptor.update({'summary':resumen})

        return self.descriptor

class PDFParser(URLObject):

    def describe(self, url=None):        

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        texto = extract_pdf(url)
        
        self.descriptor.update({'fulltext':texto})

        return self.descriptor

#response=getAtrib(response)
#data=[]
#['tags',a.tags],
#keys=['domain','author','url_hash','url','meta_keywords','meta_lang','meta_description','short_url','title','excerpt','date_published','publish_date']
#for key in keys:
#    if response!=None and key in response and response[key]!=None and len(response[key])>0:
#        rowData=[key,response[key]]
#    elif a!=None and key in dir(a) and getattr(a,key)!=None and len(getattr(a,key))>0:
#        rowData=[key,getattr(a,key)]
#    else:
#        rowData=[key,""]
#    data.append(rowData)
#return data


def getAtrib(res):
    keys=['domain','author','url','short_url','title','excerpt','date_published']
    for key in keys:
        if key not in res.viewkeys():
            res[key]=""
    return res
