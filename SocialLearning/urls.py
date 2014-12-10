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

router = routers.DefaultRouter()
router.register(r'resources', views.ResourceViewSet)
router.register(r'collections', views.CollectionViewSet)
router.register(r'mentions', views.MentionViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'relevance', views.RelevanceViewSet)
router.register(r'feeds', views.ResourceContainerViewSet)
#router.register(r'noticias', views.ResourceSearch, base_name='noticias')


#http://social.hontza.es/update/topic/", 
#http://social.hontza.es/update/collection/", 
#http://social.hontza.es/update/interest/"

update_router = routers.DefaultRouter()
update_router.register(r'collection', views.CollectionUpdateViewSet)
update_router.register(r'topic', views.TopicUpdateViewSet)
update_router.register(r'interest', views.InterestUpdateViewSet)
update_router.register(r'feed', views.ResourceContainerViewSet)

urlpatterns += patterns('',
    url(r'search/', views.ResourceSearch.as_view()),    
    url(r'update/', include(update_router.urls)), 
    url(r'api/', include(router.urls)),   
)
