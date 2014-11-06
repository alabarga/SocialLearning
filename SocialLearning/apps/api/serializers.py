from django.forms import widgets
from rest_framework import serializers
from learningobjects.models import *

class ResourceSerializer(serializers.HyperlinkedModelSerializer):

    relevance = serializers.SerializerMethodField('get_relevance')
    def get_relevance(self, obj):
        return obj.get_relevance('3Dprinting')

    class Meta:
        model = Resource
        fields = ('id', 'identifier', 'title', 'url', 'relevance')


class CollectionSerializer(serializers.HyperlinkedModelSerializer):

    resources = serializers.HyperlinkedRelatedField(many=True, view_name='resource-detail')
    class Meta:
        model = Collection
        fields = ('name','resources')        




