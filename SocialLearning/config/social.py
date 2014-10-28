
#####TWITTER KEYS#####
CONSUMER_KEY = 'ieZUZgZrSJJE0QLBBOsgXg'
CONSUMER_SECRET = 'PlIpSrh6unKYZISSDieBIFAB3D9f6aSh4p4Dmcn8Q'
OAUTH_TOKEN = '1015949947-0Akq5OBnEzTp7OwaIuvLNiKN6L52FNLVOW9yIyf'
OAUTH_TOKEN_SECRET = 'SJz3nXcyGt2lIKhmPiFg5VlTdHLbrRSPRRgUZ552xfe1e'
####Twitter auth handler####
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
twittApi = tweepy.API(auth)
####Google custom search API####
SEARCH_ENGINE_ID = '009363772985848074726:jxffracj2_8' #os.environ['SEARCH_ENGINE_ID']                          
API_KEY = 'AIzaSyCE9D6fjIW86IN2uekwJbaS3TDfNbim-lE' #os.environ['GOOGLE_CLOUD_API_KEY']
googleApi = GoogleCustomSearch(SEARCH_ENGINE_ID, API_KEY)
####Slideshare API keys####
ssapi_key = 'lKp4aIF5' # Your api key
sssecret_key = 'x7fmnUa8' # Your secret key
##########################