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
        fg.id(data['url'])
        fg.title(data['name'])
        fg.author( {'name':'SocialLearning','email':'social@hontza.es'} )
        fg.link( href=data['url'], rel='alternate' )
        fg.logo('http://www.ovtt.org/sites/default/files/styles/ampliacion_noticia/public/logo_hontza_fondo-claro_opaco.png')
        fg.subtitle(data['description'])
        fg.link( href=data['url']+'?format=rss', rel='self' )
        fg.language('en')
        
        for item in data['resources']:
            fe = fg.add_entry()
            fe.id(item['url'])
            fe.title(item['title'])

        return fg.rss_str(pretty=True)