# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',  # noqa
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),

    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),

    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here

    url(r'^redactor/', include('redactor.urls')), 
    
    url(r'^k/', include('learningobjects.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api-docs/', include('rest_framework_swagger.urls')), 
     
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework import routers
from api import views



#router.register(r'noticias', views.ResourceSearch, base_name='noticias')


#http://social.hontza.es/update/topic/", 
#http://social.hontza.es/update/collection/", 
#http://social.hontza.es/update/interest/"

import rest_framework
from rest_framework import reverse, response
class HybridRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}
    def add_api_view(self, name, url):
        self._api_view_urls[name] = url
    def remove_api_view(self, name):
        del self._api_view_urls[name]
    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._api_view_urls.keys():
            urls.append(self._api_view_urls[api_view_key])
        return urls

    def get_api_root_view(self):
        # Copy the following block from Default Router
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        api_view_urls = self._api_view_urls

        class APIRoot(rest_framework.views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse.reverse(url_name, request=request, format=format)
                # In addition to what had been added, now add the APIView urls
                for api_view_key in api_view_urls.keys():
                    ret[api_view_key] = reverse.reverse(api_view_urls[api_view_key].name, request=request, format=format)
                return response.Response(ret)

        return APIRoot.as_view()


router = HybridRouter()
router.register(r'resources', views.ResourceViewSet)
router.register(r'collections', views.CollectionViewSet)
router.register(r'mentions', views.MentionViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'relevance', views.RelevanceViewSet)
router.register(r'feeds', views.ResourceContainerViewSet)

update_router = HybridRouter()
update_router.register(r'collection', views.CollectionUpdateViewSet)
update_router.register(r'topic', views.TopicUpdateViewSet)
update_router.register(r'interest', views.InterestUpdateViewSet)
update_router.register(r'feed', views.ResourceContainerViewSet)
update_router.add_api_view('files', url(r'^files/$', views.AddFile.as_view(), name='files'))

router.add_api_view('files', url(r'^files/(?P<pk>[\d]+)/$', views.FileInstanceView.as_view(), name='file-instance'))

urlpatterns += patterns('',
    url(r'search/', views.ResourceSearch.as_view()),    
    url(r'update/', include(update_router.urls)), 
    url(r'api/', include(router.urls)),   
)
