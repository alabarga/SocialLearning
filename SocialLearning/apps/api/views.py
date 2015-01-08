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
from django_filters.fields import Lookup
from rest_framework.parsers import MultiPartParser, FormParser


# curl -X POST http://127.0.0.1:8000/update/files/ -F "name=mi otro archivo" -F "collection=1" -F "source=@/home/alabarga/Downloads/social.jpg;type=image/jpeg" -H "Content-Type: multipart/form-data" 
# curl -X POST http://social.hontza.es/update/files/ -F "name=mi otro archivo" -F "collection=1" -F "source=@/home/alabarga/Downloads/social.jpg;type=image/jpeg" -H "Content-Type: multipart/form-data" 

class FileInstanceView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns a single author.
    Also allows updating and deleting
    """
    model = File
    serializer_class = AssetSerializer

class AddFile(APIView):
    queryset = File.objects.all()
    serializer_class = AssetSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post_dos(self, request, format=None):
        my_file = request.FILES['file_field_name']
        filename = '/tmp/myfile'
        with open(filename, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)

        my_saved_file = open(filename) #there you go

    def post_original(self, request, format=None):
        serializer = AssetSerializer(data=request.DATA)
        print serializer.data

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = AssetSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        serializer = AssetSerializer(self.queryset, many=True)
        return Response(serializer.data)

#curl -X POST 127.0.0.1:8000/update/files/ -d '{"name" = "my image   ","source"="/home/alabarga/Downloads/social.jpg"}' -H "Content-Type: application/json"

#######################################################################
# Search API
#######################################################################

class ListFilter(django_filters.Filter):
    def filter(self, qs, value):
        print value
        return super(ListFilter, self).filter(qs, Lookup( [int(i) for i in value.split(',')], 'in'))

class ResourceFilter(django_filters.FilterSet):
    interest = django_filters.NumberFilter(name="_interest", lookup_type='gte')
    interest_hontza = django_filters.NumberFilter(name="interest_hontza", lookup_type='gte')
    title = django_filters.CharFilter(name="title", lookup_type='icontains')   
    socialnetwork = django_filters.CharFilter(name="seen_at__social_network__name", lookup_type='icontains')
    username = django_filters.CharFilter(name="seen_at__username", lookup_type='icontains')
    description = django_filters.CharFilter(name="description", lookup_type='icontains')
    topic = django_filters.CharFilter(name="relevant__name", lookup_type='icontains')
    relevance = django_filters.NumberFilter(name="relevant__relevance__score", lookup_type='gte')
    site = django_filters.CharFilter(name="domain", lookup_type='icontains')
    #collection = django_filters.NumberFilter(name="collection")
    #tags = django_filters.CharFilter(name="tags__name", lookup_type='icontains')
    #collection = django_filters.MultipleChoiceFilter(name="collection")
    collection = ListFilter(name='collection')
    tags = ListFilter(name='tags__name')

    class Meta:
        model = Resource
        fields = [ 'collection','title', 'description', 'tags', 'content', 'language', 'site', 'interest', 'interest_hontza', 'topic', 'relevance', 'socialnetwork', 'username']

class ResourceSearch(generics.ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceDetailSerializer
    filter_class = ResourceFilter

    """
    def get_queryset(self):

        ## Override get_queryset() to filter on multiple values for 'id'

        id_value = self.request.QUERY_PARAMS.get('id', None)
        if id_value:
            id_list = id_value.split(',')
            queryset = queryset.filter(id__in=id_list)

        return queryset
    """

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
