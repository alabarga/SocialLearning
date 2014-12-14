from learningobjects.models import *
from api.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
import django_filters


#######################################################################
# Search API
#######################################################################

class ResourceFilter(django_filters.FilterSet):
    interest = django_filters.NumberFilter(name="_interest", lookup_type='gte')
    interest_hontza = django_filters.NumberFilter(name="interest_hontza", lookup_type='gte')
    title = django_filters.CharFilter(name="title", lookup_type='icontains')
    tags = django_filters.CharFilter(name="tags__name", lookup_type='icontains')
    socialnetwork = django_filters.CharFilter(name="seen_at__social_network__name", lookup_type='icontains')
    username = django_filters.CharFilter(name="seen_at__username", lookup_type='icontains')
    description = django_filters.CharFilter(name="description", lookup_type='icontains')
    topic = django_filters.CharFilter(name="relevant__name", lookup_type='icontains')
    relevance = django_filters.NumberFilter(name="relevant__relevance__score", lookup_type='gte')
    site = django_filters.CharFilter(name="domain", lookup_type='icontains')
    collection = django_filters.NumberFilter(name="collection")

    class Meta:
        model = Resource
        fields = [ 'collection','title', 'description', 'tags', 'content', 'language', 'site', 'interest', 'interest_hontza', 'topic', 'relevance', 'socialnetwork', 'username']

class ResourceSearch(generics.ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceDetailSerializer
    filter_class = ResourceFilter

"""    
class ResourceSearch(APIView):
    #List all snippets, or create a new snippet.
    
    def get(self, request, format=None):

        interest = request.GET.get('interest', None)

        resources = Resource.objects.filter(_interest__gte=interest)
        serializer = ResourceDetailSerializer(resources, many=True, context={'request': request})
        return Response(serializer.data)
"""

#######################################################################
# View API
#######################################################################

"""
class ResourceViewSet(viewsets.ModelViewSet):

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
"""

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ResourceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ResourceDetailSerializer
        if self.action == 'retrieve':
            return ResourceDetailSerializer
        return ResourceDetailSerializer # I dont' know what you want for create/destroy/update       

class ResourceContainerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ResourceContainer.objects.all()
    serializer_class = ResourceContainerSerializer

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

class RelevanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Relevance.objects.all().order_by('-score')
    serializer_class = RelevanceSerializer   

#######################################################################
# Update API
#######################################################################

class CollectionUpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionUpdateSerializer 

class TopicUpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicUpdateSerializer 

class InterestUpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Resource.objects.all()
    serializer_class = InterestUpdateSerializer     
