from django.forms import widgets
from rest_framework import serializers
from learningobjects.models import *

class ResourceSerializer(serializers.HyperlinkedModelSerializer):

#    status = serializers.SerializerMethodField('connect_to_R')
#    def get_status(self, obj):
#        return Resource.NORMAL

    class Meta:
        model = Resource
        fields = ('identifier', 'title', 'url')




