import time
import requests
import json

API_HOST = 'http://otter.topsy.com'
API_KEY = '09C43A9B270A470B8EB8F2946A9369F3'
DEFAULT_PERPAGE = 100

try:
    from local_settings import API_KEY
except:
    pass

class Result(object):
    
    def __init__(self, request):
        self._request = request
        self._data = json.loads(request.content)
        self.request = self._data['request']
        self.__doc__ = getattr(Topsy,self.request['resource']).__doc__
        self.response = self._data['response']
        for k in self.response.keys():
            setattr(self, k, self.response[k])

    def __str__(self):
        string = 'Topsy "%s" Result:\n-----KEYS-----\n' % self.request['resource']
        string += '\n'.join(self.response.keys())
        return string

    def __repr__(self):
        return json.dumps(self.response, indent=4)

    def more(self):
        if len(self.list) >= int(self.total):
            return None
        params = self.request['parameters']
        params['page'] = int(self.page) + 1
        params['offset'] = self.last_offset
        params['apikey'] = API_KEY
        url = self.request['url'].split('?')[0].replace('http://api-int:7000',API_HOST)
        request = requests.get(url, params=params)
        self._request = request
        self._data = json.loads(request.content)
        self.request = self._data['request']
        self.response = self._data['response']
        for k in self.response.keys():
            if k == 'list':
                setattr(self, k, getattr(self, k) + self.response[k])
            else:
                setattr(self, k, self.response[k])


class Topsy(object):
    '''
        Full API Documentation: http://code.google.com/p/otterapi/wiki/Resources

        All requests are implemented via HTTP GET calls. 
        The url of the request can be broken down into three parts: 
        Resources (described below), response format, and query parameters. 
        A malformed request will return a response with HTTP 400 status.

    '''
    
    def __init__(self, api_key=''):
        self._api_key = api_key or API_KEY
        self._api_host = API_HOST
        self._rate_limit = 0
        self._rate_limit_remaining = 0
        self._rate_limit_reset = 0

    def _get(self, resource='', **params):
        params['apikey'] = self._api_key
        url = '%s/%s.json' % (self._api_host, resource)
        r = requests.get(url, params=params)
        return Result(request=r)

    def more(self, result):
        '''return the next page of results, if possible, or nothing''' 
        if len(result.list) < int(result.perpage):
            return None
        resource = result.request['resource']
        params = result.request['parameters']
        params['page'] = int(params.get('page', 1)) + 1
        params['offset'] = result.response['last_offset']
        return self._get(resource, **params)

    @property
    def remaining(self):
        return int(self._rate_limit_remaining)

    @property
    def reset(self):
        '''how many hours until the rate_limit_remaining resets?'''
        diff_secs = int(self._rate_limit_reset) - int(time.time())
        diff_hours = diff_secs / (60 * 60.0)
        return diff_hours

    def authorinfo(self, nick=''):
        '''
            
            Profile information for an author (a twitter profile indexed by Topsy). The response contains 
            the name, description (biography) and the influence level of the author.

             nick     |  required    |  Twitter handel for the author. 

        '''
        url = 'http://twitter.com/%s' % nick
        return self._get('authorinfo', url=url)

    def experts(self, query='', **params):
        '''
            
            List of authors that talk about the query. The list is sorted by frequency of 
            posts and the influence of authors. (Note: for backwards compatibility, 
            the /authorsearch api method is an alias to /experts.)

             q                  |  required    |  Search query string. (query syntax)  | query syntax
             config_NoFilters   |  optional  |  Setting this to 1, would turn off all other filters. Default value is 0. 

        '''
        return self._get('experts', q=query, **params)

    def populartrackbacks(self, url):
        '''
            
            List of most popular and unique tweets (trackbacks) that mention the query URL.

             url       |  required    |  URL string for the target. 

        '''
        return self._get('populartrackbacks', url=url)

    def linkposts(self, nick='', contains='', tracktype=''):
        '''
            
            List of urls posted by an author.

             url       |  required    |  URL string for the author. 
             contains  |  optional    |  A query filter for linkposts (the content must contain this string). 
             tracktype |  optional    |  Type of posts. (image, tweet__various, self__tweet)

        '''
        url = 'http://twitter.com/%s' % nick
        return self._get('linkposts', url=url, contains=contains,
            tracktype=tracktype)

    def linkpostcount(self, nick='', contains='', tracktype=''):
        '''
            
            Count of links posted by an author. This is the efficient, count-only version of /linkposts

             url       |  required    |  URL string for the author. 
             contains  |  optional    |  Query string to filter results. 
             tracktype |  optional    |  Type of posts. (image, tweet__various, self__tweet)

        '''
        url = 'http://twitter.com/%s' % nick
        return self._get('linkpostcount', url=url, contains=contains,
            tracktype=tracktype)

    def search(self, q='', **params):
        '''
            
            List of results for a query.

             q               |  required    |  Search query string. (query syntax)  | query syntax
             window          |  optional    |  Time window for results. (Options: dynamic (most relevant). Must be 1-23 hours or 1-100 days (h6 or d10). h: hour, d: day, w: week, m: month, a: all-time. 
             type            |  optional    |  The type of result.  Default is nothing, which includes all types.  Other supported values are image, tweet and video | image | tweet | video
             query_features  |  optional    |  Enables QueryFeatures described in the wiki. Only works when window=dynamic  | QueryFeatures

        '''
        return self._get('search', q=q, perpage=DEFAULT_PERPAGE,
                **params)

    def searchcount(self, q='', dynamic=''):
        '''
            
            Count of results for a search query.

             q         |  required    |  Search query string. (query syntax)  | query syntax
             dynamic   |  optional    |  If the value equals 1, the response will contain an extra window that is the best window for the given query. The possible responses are h1 through h23, or d1 through d100. These represent hourly or daily increments. NOTE: the output format of the response will change when this parameter is used. 

        '''
        return self._get('searchcount', q=q, dynamic=dynamic)

    def searchhistogram(self, q='', slice='86400', period='30', 
        count_method='target'):
        '''
            
            The searchhistogram provides information to determine when a particular keyword peaked in the past days.

             q             |  required    |  Search query string. (query syntax)  | query syntax
             slice         |  optional    |  The number of seconds for each slice. Defaults to 86400 (1 day) 
             period        |  optional    |  The number of slices.  Defaults to 30 (1 month) 
             count_method  |  options     |  This has two possible values, the default is "target" and the other possible value is "citation".  count_method specifies what is being counted, "target" means the number of unique links and "citation" means the number of unique tweets about links. 

        '''
        return self._get('searchhistogram', q=q, slice=slice,
            period=period, count_method=count_method)

    def searchdate(self, q='', window='', type='', zoom=10):
        '''
            
            Returns search results sorted by reverse chronology. All options are the same as that of /search.

             q        |  required    |  Search query string. (query syntax)  | query syntax
             window   |  optional    |  See /search documentation. 
             type     |  optional    |  See /search documentation. 
             zoom     |  optional    |  Zoom-level for depth / quality.  Default is 10, which picks 100 results 

        '''
        return self._get('search', q=q, window=window, type=type,
            zoom=zoom)

    def stats(self, url='', contains=''):
        '''
            
            Count of tweets for a url. This is an efficient way of getting the counts only. 
            For detailed information about a URL, use urlinfo.

             url       |  required    |  URL string for the target. 
             contains  |  optional    |  A query filter for trackbacks (the trackbacks must contain this string). 

        '''
        return self._get('stats', url=url, contains=contains)

    def top(self, thresh='top100', type='', locale=''):
        '''
            
            A feed of Top 100, 1K, 5K and 20K links, photos, tweets & videos posted on the social web everyday.

             thresh    |  required    |  top100, top1k, top5k, top20k 
             type      |  optional    |  defaults to everything. Other values: image, video, tweet 
             locale    |  optional    |  defaults to all.  Other values:  en, ja, ko, de, pt, es, th, fr 

        '''
        if thresh not in ['top100', 'top1k', 'top5k', 'top20k']:
            thresh = 'top100'
        if type not in ['', 'image', 'video', 'tweet']:
            type = ''
        if locale not in ['', 'en', 'ja', 'ko', 'de', 'pt', 'es', 'th', 'fr']:
            locale = ''
        return self._get('top', thresh=thresh, type=type, locale=locale)

    def trackbacks(self, url='', contains='', ifonly='', sort_method=''):
        '''
            
            List of tweets (trackbacks) that mention the query URL, most recent first.

             url           |  required    |  URL for the target. 
             contains      |  optional    |  Query string to filter results. 
             infonly       |  optional    |  Boolean value that filters trackbacks to influential only (default 0) 
             sort_method   |  optional    |  the order in which to return results. Options are "influence", "date" and "-date". 

        '''
        return self._get('trackbacks', url=url, contains=contains,
            ifonly=ifonly, sort_method=sort_method)

    def urlinfo(self, url=''):
        '''
            
            Information about an url.

             url       |  required    |  URL string for the target. 

        '''
        return self._get('urlinfo', url=url)
