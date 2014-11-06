from django.forms import widgets
from rest_framework import serializers
from learningobjects.models import *

class ResourceSerializer(serializers.HyperlinkedModelSerializer):

    interest = serializers.SerializerMethodField('get_interest')
    mentions = serializers.HyperlinkedIdentityField(view_name='mention-detail')

    def get_interest(self, obj):
        return obj.get_interest()

    class Meta:
        model = Resource
        fields = ('id', 'title', 'description', 'url', 'interest', 'mentions')

class CollectionSerializer(serializers.HyperlinkedModelSerializer):

    resources = serializers.HyperlinkedIdentityField(view_name='resource-detail')
    class Meta:
        model = Collection
        fields = ('name','resources')        

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    
    social_network = serializers.RelatedField()
    class Meta:
        model = SocialProfile
        fields = ('social_network', 'username',)

class MentionSerializer(serializers.HyperlinkedModelSerializer):

    profile = serializers.RelatedField()
    resource = serializers.HyperlinkedRelatedField(view_name='resource-detail')

    class Meta:
        model = Mention
        fields = ('profile','resource')          




