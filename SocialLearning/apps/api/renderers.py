from rest_framework import renderers
from feedgen.feed import FeedGenerator

class RSSRenderer(renderers.BaseRenderer):
    """
    Renderer which serializes to CustomXML.
    """

    media_type = 'application/xml'
    format = 'rss'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders *obj* into serialized XML.
        """
        if data is None:
            return ''
        
        fg = FeedGenerator()
        myclass = type(renderer_context['view']).__name__ 

        print renderer_context['request']
        print myclass

        if myclass == 'CollectionViewSet':
           
            feed_url = data['url']
            feed_title = data['name']
            feed_description = data['description']
            resources = data['resources']
        elif myclass == 'ResourceViewSet':
            feed_url = "http://social.honzta.es/api/resources/"
            feed_title = "SocialLearning resources"
            feed_description = "SocialLearning resources"
            resources = data
        else: 
            feed_url = "http://social.honzta.es/api/resources/"
            feed_title = "SocialLearning resources"
            feed_description = "SocialLearning resources"
            resources = []
        
        fg.id(feed_url)
        fg.title(feed_title)
        fg.subtitle(feed_description)
        fg.author( {'name':'SocialLearning','email':'social@hontza.es'} )
        fg.link( href=feed_url, rel='alternate' )
        fg.logo('http://www.ovtt.org/sites/default/files/styles/ampliacion_noticia/public/logo_hontza_fondo-claro_opaco.png')        
        fg.link( href=feed_url+'?format=rss', rel='self' )
        fg.language('en')

        for item in resources:
            fe = fg.add_entry()
            fe.id(item['url'] or 'http://social.honzta.es/api/resources/1/')
            fe.title(item['title'] or 'title')
            #fe.link(item['url'])
            #fe.content(item['title'])
            #fe.description(item['description'])

        return fg.rss_str(pretty=True)