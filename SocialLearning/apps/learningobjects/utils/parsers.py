from __future__ import unicode_literals
from ftfy import fix_text

import readability
from goose import Goose
from pyteaser import SummarizeUrl
import requests

from learningobjects.utils.pdf import extract_pdf
from learningobjects.utils import youtube
import unfurl
from urlunshort import resolve

###Readability parser

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


class URLObject(object):

    def clean2(self, url):
        furl=url
        i=0
        while resolve(url)!=None and i<5:
            furl=url
            url=resolve(url)
            i+=1
            print i
        return furl

    def clean(self, url):

        try:
            furl = expand_url(url)
        except:
            furl = url

        return furl
        
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
            self.url = self.clean(url)
            self.descriptor = dotdict({'url':self.url})

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

#https://gdata.youtube.com/feeds/api/videos/MLK-_4Vb8Iw/captions&access_token=AIzaSyDQjDxSwnFVVvUmaZPJMhOJd0bbTRVIU48
#http://video.google.com/timedtext?lang=en&v=MLK-_4Vb8Iw
#http://www.serpsite.com/transcript.php?videoid=https://www.youtube.com/watch?v=MLK-_4Vb8Iw
#http://stackoverflow.com/questions/14061195/how-to-get-transcript-in-youtube-api-v3
#https://gdata.youtube.com/feeds/api/videos/MLK-_4Vb8Iw/captions&access_token=AIzaSyDQjDxSwnFVVvUmaZPJMhOJd0bbTRVIU48
#http://video.google.com/timedtext?lang=en&v=MLK-_4Vb8Iw
#http://www.serpsite.com/transcript.php?videoid=https://www.youtube.com/watch?v=MLK-_4Vb8Iw
#http://stackoverflow.com/questions/14013431/extract-automatic-captions-from-youtube-video
#http://video.google.com/timedtext?hl=en&v=bgvrYAXjQHI&lang=en&type=text
#https://www.youtube.com/api/timedtext?v=MLK-_4Vb8Iw&type=track&lang=en&name&kind=asr&fmt=1
#v=MLK-_4Vb8Iw
#&hl=es-ES
#&signature=F08A79C29F199C9EF7E17BDA9DAC1D1000D7EE81.B0F3417880C31FFC7B4F8DDA50FE83CC79D8B9EA
#&caps=asr
#&sparams=asr_langs%2Ccaps%2Cv%2Cexpire&key=yttt1
#&expire=1417039177
#&asr_langs=en%2Cde%2Cko%2Cja%2Cru%2Cfr%2Cnl%2Cpt%2Cit%2Ces
#http://www.serpsite.com/transcript.php?videoid=https://www.youtube.com/watch?v=MLK-_4Vb8Iw

class YoutubeParser(URLObject):

    def describe(self, url=None):        

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        video = youtube.new(url)
        video.url = url
        self.descriptor = video

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
