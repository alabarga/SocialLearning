from sharegg.social import Counter, Followers, Shares

import os

fb_token = os.environ.get('FB_TOKEN', '396834553717492|vMmcYpVU8zBTQk_a3aG9061tTiw')
gplus_key = os.environ.get('GPLUS_KEY', 'AIzaSyDQjDxSwnFVVvUmaZPJMhOJd0bbTRVIU48')

twitter_auth = {
    'api_key': os.environ.get('TWITTER_API_KEY', 'ieZUZgZrSJJE0QLBBOsgXg'),
    'api_secret': os.environ.get('TWITTER_API_SECRET', 'PlIpSrh6unKYZISSDieBIFAB3D9f6aSh4p4Dmcn8Q'),
    'token_key': os.environ.get('TWITTER_TOKEN_KEY', '1015949947-0Akq5OBnEzTp7OwaIuvLNiKN6L52FNLVOW9yIyf'),
    'token_secret': os.environ.get('TWITTER_TOKEN_SECRET', 'SJz3nXcyGt2lIKhmPiFg5VlTdHLbrRSPRRgUZ552xfe1e'),
}