from google_search import GoogleCustomSearch
import sha
import xml.etree.ElementTree as ET
import unfurl
import urllib2

class SearchEngine(object):

    def __init__(self, engine):
        self.engine = engine


    def clean(self,url):
        
        try:
           url=unfurl.expand_url(url)           
        except (RuntimeError, TypeError, NameError):
           pass

        return url

class Google(SearchEngine):
    def __init__(self):
        super(DuckDuckGo, self).__init__("google")

    #Busca en google con los parametros que se pasen
    def search(query):
        links=[]        

        SEARCH_ENGINE_ID = '009363772985848074726:jxffracj2_8' #os.environ['SEARCH_ENGINE_ID']                          
        API_KEY = 'AIzaSyCE9D6fjIW86IN2uekwJbaS3TDfNbim-lE' #os.environ['GOOGLE_CLOUD_API_KEY']
        googleApi = GoogleCustomSearch(SEARCH_ENGINE_ID, API_KEY)

        for result in googleApi.search(query):
          link=result['link']
          if link not in links:

            links.insert(0,link)
        return links

class DuckDuckGoIO(SearchEngine):

    def __init__(self):
        super(DuckDuckGo, self).__init__("duckduckgo")

    #Busca en duckduck con los parametros que se pasen
    def search(query):
        links=[]        
        IMPORTIO_USER = "7d0326db-696a-436d-8aba-f6c2e1c9e921"
        IMPORTIO_API_KEY = "89Gl8Ce2tiqX949GcKQTE9hCg6NW%2FkN36WpGKEA4knjhoTTRT72%2BitSWPicKFsZ4RmTwvyMbC%2BOrPtxAvy1EGw%3D%3D"
        url="https://api.import.io/store/data/97e350d1-d55c-4c66-bcc4-5c2bd2eb8765/_query?input/query="+query+"&_user="+IMPORT_IO_USER+"&_apikey="+IMPORTIO_API_KEY
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
        super(DuckDuckGo, self).__init__("slideshare")

    def search(query):

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