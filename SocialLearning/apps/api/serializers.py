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

class RelevanceSerializer(serializers.HyperlinkedModelSerializer):

    topic = serializers.HyperlinkedRelatedField(view_name='topic-detail')    #serializers.RelatedField() 
    resource = serializers.HyperlinkedRelatedField(view_name='resource-detail') #ResourceIdSerializer()

    class Meta:
        model = Relevance
        fields = ('resource', 'topic', 'score')  

class ResourceRelevanceSerializer(serializers.HyperlinkedModelSerializer):
 
    resource = serializers.HyperlinkedRelatedField(view_name='resource-detail') #ResourceIdSerializer()

    class Meta:
        model = Relevance
        fields = ('resource', 'score')  

class TopicRelevanceSerializer(serializers.HyperlinkedModelSerializer):

    topic = serializers.HyperlinkedRelatedField(view_name='topic-detail')    #serializers.RelatedField() 
    resource = serializers.HyperlinkedRelatedField(view_name='resource-detail') #ResourceIdSerializer()

    class Meta:
        model = Relevance
        fields = ('topic', 'score')  

class ResourceSerializer(serializers.HyperlinkedModelSerializer):

    interest = serializers.SerializerMethodField('get_interest')

    mentions = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                   view_name='mention-detail')

    topics = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='relevance-detail')

    # resource = serializers.CharField(source='get_absolute_url', read_only=True)

    #resource = serializers.HyperlinkedIdentityField(
    #    view_name='resource_detail',
    #    lookup_field='identifier'
    #)

    def get_interest(self, obj):
        return obj.interest

    class Meta:
        model = Resource
        url_field_name = 'resource'
        fields = ('resource','title', 'description', 'url', 'interest', 'mentions', 'topics')


class ResourceListSerializer(serializers.HyperlinkedModelSerializer):

    interest = serializers.SerializerMethodField('get_interest')

    topic_list = serializers.SerializerMethodField('get_topics')

    mentions = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                   view_name='mention-detail')

    #topics = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                                view_name='relevance-detail')

    # resource = serializers.CharField(source='get_absolute_url', read_only=True)

    #resource = serializers.HyperlinkedIdentityField(
    #    view_name='resource_detail',
    #    lookup_field='identifier'
    #)

    def get_interest(self, obj):
        return obj.interest

    def get_topics(self, obj):
        return obj.topic_list

    class Meta:
        model = Resource
        url_field_name = 'resource'
        fields = ('resource', 'url', 'title', 'description', 'interest', 'topic_list')

class ResourceDetailSerializer(serializers.HyperlinkedModelSerializer):

    interest = serializers.SerializerMethodField('get_interest')

    topic_list = serializers.SerializerMethodField('get_topics')

    mentions = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                       view_name='mention-detail')

    #topics = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                                 view_name='relevance-detail')

    topics = TopicRelevanceSerializer(many=True, read_only=True)

    # resource = serializers.CharField(source='get_absolute_url', read_only=True)

    #resource = serializers.HyperlinkedIdentityField(
    #    view_name='resource_detail',
    #    lookup_field='identifier'
    #)

    def get_interest(self, obj):
        return obj.interest

    def get_topics(self, obj):
        return obj.topic_list

    class Meta:
        model = Resource
        url_field_name = 'resource'
        fields = ('resource', 'url', 'title', 'description', 'interest', 'topic_list', 'topics', 'mentions')


class ResourceIdSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resource
        fields = ('id', 'title')

class ResourceContainerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ResourceContainer
        fields = ('name', 'url','rss')


class TopicSerializer(serializers.HyperlinkedModelSerializer):

    relevance = ResourceRelevanceSerializer(many=True)
    tags = TagListSerializer(blank=True)

    class Meta:
        model = Topic
        url_field_name = 'topic'
        fields = ('topic', 'name', 'relevance')

class CollectionSerializer(serializers.HyperlinkedModelSerializer):

    resources = serializers.HyperlinkedIdentityField(view_name='resource-detail')
    class Meta:
        model = Collection
        fields = ('name','resources')        

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    
    social_network = serializers.RelatedField()
    class Meta:
        model = SocialProfile
        fields = ('url','social_network', 'username',)

class MentionSerializer(serializers.HyperlinkedModelSerializer):

    profile = serializers.HyperlinkedRelatedField(view_name='socialprofile-detail') #serializers.RelatedField()
    resource = serializers.HyperlinkedRelatedField(view_name='resource-detail')

    mention = serializers.SerializerMethodField('get_username')
    def get_username(self, obj):
        return obj.__unicode__

    class Meta:
        model = Mention
        url_field_name = 'mention_url'
        fields = ('mention_url', 'profile','resource', 'mention','card')          




