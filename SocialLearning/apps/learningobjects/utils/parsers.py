import readability
from goose import Goose
from pyteaser import SummarizeUrl

###Readability parser

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


class URLObject(object):

    def __init__(self, url):
        self.url = url


class ReadibilityParser(URLObject):

    parser = readability.ParserClient('03b5d5676456982e868cf57e5b6757f198ef479d')

    def describe(url=None):

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        # Readability
        try:
            response=self.parser.get_article_content(url.encode('utf-8'))
            a = dotdict(response.content)
        except:
            a = dotdict({'url':url})

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

        return a

class GooseParser(URLObject):

    def describe(url=None):

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        #Goose
        g = Goose()
        try:
            a = g.extract(url=url.encode('utf-8'))  
        except:
            a = dotdict({'url':url})

        a.url = url

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

class TeaserParser(URLObject):

    def describe(url=None):        

        if url == None:
            url = self.url

        if url == None:    
            print "No URL provided"
            return

        summaries=SummarizeUrl(url.encode('utf-8'))

        resumen = ''
        for s in summaries:
            resumen += s

        a = dotdict({'url':url,'excerpt':resumen})

        return a

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
