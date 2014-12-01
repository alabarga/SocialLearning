import json
import urllib
import urllib2

APPLICATION_ID = '2e4bb84a'
APPLICATION_KEY = '336b9a4229920f9e0110fb916765a6bc'

class AylienAPI(object):

    def call_api(self, endpoint, parameters):
        url = 'https://api.aylien.com/api/v1/' + endpoint
        headers = {
            "Accept":                             "application/json",
            "Content-type":                       "application/x-www-form-urlencoded",
            "X-AYLIEN-TextAPI-Application-ID":    APPLICATION_ID,
            "X-AYLIEN-TextAPI-Application-Key":   APPLICATION_KEY
        }
        opener = urllib2.build_opener()
        request = urllib2.Request(url, urllib.urlencode(parameters), headers)
        response = opener.open(request);
        return json.loads(response.read())


    def extract(self, text=None, url=None):

        if url:
            parameters = {"text": text}   
        else:       
            parameters = {"url": url}

        descriptor = self.call_api("extract", parameters)
        return descriptor

    def sentiment(self, text=None, url=None):

        if url:
            parameters = {"text": text}   
        else:       
            parameters = {"url": url}

        sentiment = self.call_api("sentiment", parameters)
        return sentiment

    def language(self, text=None, url=None):        
        if url:
            parameters = {"text": text}   
        else:       
            parameters = {"url": url}

        language = self.call_api("language", parameters)

        return

#sentiment = AylienAPI.sentiment("http://www.elmundo.es/espana/2014/11/27/5477550722601db8758b4571.html")
#print "Sentiment: %s (%F)" % (sentiment["polarity"], sentiment["polarity_confidence"])
#print "Language: %s (%F)" % (language["lang"], language["confidence"])
