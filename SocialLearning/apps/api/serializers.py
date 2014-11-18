from django.forms import widgets
from rest_framework import serializers
from learningobjects.models import *


class TagListSerializer(serializers.WritableField):

    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")     
        return data
    
    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj

class ResourceSerializer(serializers.HyperlinkedModelSerializer):

    interest = serializers.SerializerMethodField('get_interest')
    
    mentions = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                   view_name='mention-detail')

    relevance = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='relevance-detail')

    def get_interest(self, obj):
        return obj.get_interest()

    class Meta:
        model = Resource
        fields = ('id', 'title', 'description', 'url', 'interest', 'mentions', 'relevance')


class ResourceIdSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resource
        fields = ('id', 'title')

class RelevanceSerializer(serializers.HyperlinkedModelSerializer):

    topic = serializers.RelatedField()
    resource = ResourceIdSerializer()

    class Meta:
        model = Relevance
        fields = ('resource', 'score')  

class TopicSerializer(serializers.HyperlinkedModelSerializer):

    relevance = RelevanceSerializer(many=True)
    tags = TagListSerializer(blank=True)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'relevance')

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




