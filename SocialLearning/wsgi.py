"""
WSGI config for  project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = ".settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
os.environ.setdefault("DJANGO_SECRET_KEY", "l2gp7#914p!91#bb7t^dxj0ol2-0_6ubn@o3wj(np6w8hzoky-")

os.environ.setdefault("TWITTER_API_KEY",'ieZUZgZrSJJE0QLBBOsgXg')
os.environ.setdefault("TWITTER_API_SECRET",'PlIpSrh6unKYZISSDieBIFAB3D9f6aSh4p4Dmcn8Q')
os.environ.setdefault("TWITTER_TOKEN_KEY",'1015949947-0Akq5OBnEzTp7OwaIuvLNiKN6L52FNLVOW9yIyf')
os.environ.setdefault("TWITTER_TOKEN_SECRET", 'SJz3nXcyGt2lIKhmPiFg5VlTdHLbrRSPRRgUZ552xfe1e')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)