from learningobjects.utils.google import search as search_google
import sha
import xml.etree.ElementTree as ET
import unfurl
import urllib2, urllib
import json
import time
from urlunshort import resolve
import wikipedia

class SearchEngine(object):

    def __init__(self, engine):
        self.engine = engine


    def clean(self,url):
        furl=url
        i=0
        while resolve(url)!=None and i<5:
            furl=url
            url=resolve(url)
            i+=1
            print i
        return furl

"""
from GoogleScraper import scrape_with_config, GoogleSearchError
from GoogleScraper.database import ScraperSearch, SERP, Link

class GoogleScrape(SearchEngine):

    def __init__(self):

        super(GoogleScrape, self).__init__("GoogleScrape")

    def search(self, query):

        # See in the config.cfg file for possible values
        config = {
            'SCRAPING': {
                'use_own_ip': 'True',
                'keyword': query,
                'search_engine': 'duckduckgo'
            },
            'SELENIUM': {
                'sel_browser': 'chrome',
            },
            'GLOBAL': {
                'do_caching': 'True'
            }
        }
        try:
            sqlalchemy_session = scrape_with_config(config)
        except GoogleSearchError as e:
            print(e)

        # let's inspect what we got
        links = []
        for search in sqlalchemy_session.query(ScraperSearch).all():
            for serp in search.serps:
                print(serp)
                for link in serp.links:
                    links.append(link)
                    print(link)

        return links
"""

class Delicious(SearchEngine):

    def __init__(self):
        super(Delicious, self).__init__("delicious")

    #Busca en google con los parametros que se pasen
    def search(self,query):

        url="http://feeds.delicious.com/v2/json/tag/"+query+"?count=100"
        response=urllib2.urlopen(url)
        resp=json.loads(response.read())
        links=[]
        for res in resp:
            links.insert(0,res["u"])
        return links                

class Google(SearchEngine):
    def __init__(self):
        super(Google, self).__init__("google")

    #Busca en google con los parametros que se pasen
    def search(self,query):
        links=[]        

        for result in search_google(query):
            links.append(result)

        return links

class XGoogle(SearchEngine):
    
    def __init__(self):
        super(XGoogle, self).__init__("xgoogle")

    #Busca en google con los parametros que se pasen
    def search(self,query):
        from xgoogle.search import GoogleSearch, SearchError
        links = []
        try:
            gs = GoogleSearch(query)
            gs.results_per_page = 50
            results = gs.get_results()
            for res in results:
                links.append(res.url.encode('utf8'))
                print res.title.encode('utf8')
                print res.desc.encode('utf8')
                print res.url.encode('utf8')
        except SearchError:
            print "Search failed!"

        return links


"""
class Google(SearchEngine):
    def __init__(self):
        super(Google, self).__init__("google")

    #Busca en google con los parametros que se pasen
    def search(self,query):
        links=[]        

        SEARCH_ENGINE_ID = '009363772985848074726:jxffracj2_8' #os.environ['SEARCH_ENGINE_ID']                          
        API_KEY = 'AIzaSyCE9D6fjIW86IN2uekwJbaS3TDfNbim-lE' #os.environ['GOOGLE_CLOUD_API_KEY']
        googleApi = GoogleCustomSearch(SEARCH_ENGINE_ID, API_KEY)
        for result in googleApi.search(query):
          link=result['link']
          if link not in links:

            links.insert(0,link)
        return links

"""

class Wikipedia(SearchEngine):

    def __init__(self):
        super(Wikipedia, self).__init__("wikipedia")   

    def search(self,query):
        links = []
        wikipedia.set_lang("es")
        ids = wikipedia.search(query)
        for id in ids:
            wiki = wikipedia.page(id)
            refs = wiki.references
            links.extend(refs)

        return links

class DuckDuckGo(SearchEngine):

    def __init__(self):
        super(DuckDuckGo, self).__init__("duckduckgo")   

    def search(self,query):

        links = []
        for i in [0]:
            time.sleep(2)
            url = "https://duckduckgo.com/d.js?q=%s&l=es-es&p=1&s=%d" % (urllib.quote_plus(query), i)

            res = urllib2.urlopen(url).read()
            h = re.findall('{.*?}', res)
            n = len(h) - 1
            enlaces = json.loads('['+ (','.join(h[1:n])) + ']')
            
            for item in enlaces:
                links.append(item['c'])

    def related(self,url):

        return self.search('related:'+url)

class DuckDuckGoAPI(SearchEngine):

    def __init__(self):
        super(DuckDuckGoIO, self).__init__("duckduckgo")   

    def search(self,query):
        import json
        import urllib.request
        url = "http://api.duckduckgo.com/?q=%s&format=json&pretty=1" % urllib.quote(query)
        get_ddg = urllib.request.urlopen(url)
        ddg_read = get_ddg.read()
        ddg_read_decode = json.loads(ddg_read.decode('utf-8'))
        ddg_read = ddg_read_decode
        json_string = json.dumps(ddg_read,sort_keys=True,indent=2)
        print(json_string)
        ddg_topics = ddg_read['RelatedTopics']
        for item in ddg_topics:
            print(item['FirstURL'])

class DuckDuckGoIO(SearchEngine):

    def __init__(self):
        super(DuckDuckGoIO, self).__init__("duckduckgo")            

    #Busca en duckduck con los parametros que se pasen
    def search(self,query):
        links=[]        
        IMPORT_IO_USER = "7d0326db-696a-436d-8aba-f6c2e1c9e921"
        IMPORTIO_API_KEY = "89Gl8Ce2tiqX949GcKQTE9hCg6NW%2FkN36WpGKEA4knjhoTTRT72%2BitSWPicKFsZ4RmTwvyMbC%2BOrPtxAvy1EGw%3D%3D"
        url="https://api.import.io/store/data/97e350d1-d55c-4c66-bcc4-5c2bd2eb8765/_query?input/query="+urllib.quote(query)+"&_user="+IMPORT_IO_USER+"&_apikey="+IMPORTIO_API_KEY

        response=urllib2.urlopen(url)
        res=response.read()
        res=json.loads(res)
        res=res['results']
        for li in res:
          link=li['url']
          if link not in links:
            links.insert(0,link)
        return links         


# https://api.import.io/store/data/2297660e-b775-433d-a408-8fb6d7a808e7/_query?input/webpage/url=http%3A%2F%2Fwefollow.com%2Finterest%2F3dprinting%2F62-100&_user=7d0326db-696a-436d-8aba-f6c2e1c9e921&_apikey=89Gl8Ce2tiqX949GcKQTE9hCg6NW%2FkN36WpGKEA4knjhoTTRT72%2BitSWPicKFsZ4RmTwvyMbC%2BOrPtxAvy1EGw%3D%3D
class Slideshare(SearchEngine):

    def __init__(self):
        super(Slideshare, self).__init__("slideshare")

    def search(self,query):

        ####Slideshare API keys####
        ssapi_key = 'lKp4aIF5' # Your api key
        sssecret_key = 'x7fmnUa8' # Your secret key

        links=[]  
        ts = int(time.time())
        time_hash=sha.new(sssecret_key + str(ts)).hexdigest()   
        if query!="":
            url="https://www.slideshare.net/api/2/search_slideshows?q="+query+"&api_key="+ssapi_key+"&hash="+time_hash+"&ts="+str(ts)
        elif tag!="":
            url="https://www.slideshare.net/api/2/get_slideshows_by_tag?tag="+tag+"&limit=10&api_key="+ssapi_key+"&hash="+time_hash+"&ts="+str(ts)
        else: 
            print "error"

        response=urllib2.urlopen(url)
        res=response.read()
        #print res
        root = ET.fromstring(res)
        for child in root:
            try:
                link=child[5].text
                if link not in links:
                    links.insert(0,link)
            except:
                pass   
        return links    

class Yahoo(SearchEngine):
    
    def __init__(self):
        super(Yahoo, self).__init__("yahoo")

    def search(self,query):
        url='http://pipes.yahoo.com/pipes/pipe.run?_id=nHNB8TJm3BGumlGA9YS63A&_render=json&searchInput='+query
        res=urllib2.urlopen(url)
        res=res.read()
        res=json.loads(res)
        response=res["value"].values()[3]#los resultados
        links=[]
        for r in response:
            if r["link"] not in links:
                links.append(r["link"])
        return links
