from learningobjects.models import *
from api.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets

class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer  

class MentionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer      

class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer  

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SocialProfile.objects.all()
    serializer_class = ProfileSerializer         
