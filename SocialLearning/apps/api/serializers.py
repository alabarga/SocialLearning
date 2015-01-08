from django.forms import widgets
from rest_framework import serializers
from learningobjects.models import *


#######################################################################
# View API
#######################################################################

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
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, obj):
        return obj.topic.name

    class Meta:
        model = Relevance
        fields = ('resource', 'name', 'score')  

class TopicShortSerializer(serializers.HyperlinkedModelSerializer):

    #topic = serializers.HyperlinkedRelatedField(view_name='topic-detail')    #serializers.RelatedField() 
    #resource = serializers.HyperlinkedRelatedField(view_name='resource-detail') #ResourceIdSerializer()

    name = serializers.SerializerMethodField('get_name')

    def get_name(self, obj):
        return obj.topic.name

    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        return [tag.name for tag in obj.topic.tags.all()] 

    class Meta:
        model = Relevance
        fields = ('name', 'tags', 'score')  

class TopicRelevanceSerializer(serializers.HyperlinkedModelSerializer):

    topic = serializers.HyperlinkedRelatedField(view_name='topic-detail')    #serializers.RelatedField() 
    resource = serializers.HyperlinkedRelatedField(view_name='resource-detail') #ResourceIdSerializer()

    name = serializers.SerializerMethodField('get_name')

    def get_name(self, obj):
        return obj.topic.name

    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        return [tag.name for tag in obj.topic.tags.all()] 

    class Meta:
        model = Relevance
        fields = ('topic', 'name', 'tags', 'score')  

class MentionShortSerializer(serializers.HyperlinkedModelSerializer):

    mention = serializers.SerializerMethodField('get_username')
    def get_username(self, obj):
        return obj.__unicode__

    class Meta:
        model = Mention
        fields = ('mention','card')            
        
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

    topics = TopicRelevanceSerializer(many=True, read_only=True)
    # resource = serializers.CharField(source='get_absolute_url', read_only=True)

    mentions = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                       view_name='mention-detail')
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
        fields = ('resource', 'url', 'title', 'description', 'interest', 'topic_list', 'topics','mentions')

class ResourceDetailSerializer(serializers.HyperlinkedModelSerializer):

    interest = serializers.SerializerMethodField('get_interest')

    topic_list = serializers.SerializerMethodField('get_topics')

    #mentions = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                                   view_name='mention-detail')

    #collection = serializers.HyperlinkedRelatedField(view_name='collection-detail')
    #topics = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                                 view_name='relevance-detail')


    mentions = MentionShortSerializer(many=True, read_only=True)

    topics = TopicShortSerializer(many=True, read_only=True)

    tags = TagListSerializer(required=False)

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
        fields = ('resource', 'collection','url', 'title', 'description', 'status', 'tags', 'interest', 'interest_hontza','interest_social','interest_resource', 'topic_list', 'topics', 'mentions')        

class ResourceMongoSerializer(serializers.ModelSerializer):

    interest = serializers.SerializerMethodField('get_interest')

    topic_list = serializers.SerializerMethodField('get_topics')

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


class ResourceURLSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resource
        url_field_name = 'resource'
        fields = ('resource', 'title', 'url')

class ResourceIdSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resource
        fields = ('id', 'title')

class ResourceContainerSerializer(serializers.HyperlinkedModelSerializer):

    collection = serializers.HyperlinkedRelatedField(view_name='collection-detail', many=True)
    class Meta:
        model = ResourceContainer
        url_field_name = 'container'
        fields = ('container', 'collection', 'name', 'url', 'rss')

class TopicSerializer(serializers.HyperlinkedModelSerializer):

    relevance = ResourceRelevanceSerializer(many=True)
    tags = TagListSerializer(required=False)

    class Meta:
        model = Topic
        url_field_name = 'topic'
        fields = ('topic', 'name', 'tags', 'relevance')

class TopicDetailSerializer(serializers.HyperlinkedModelSerializer):

    tags = TagListSerializer(required=False)

    class Meta:
        model = Topic
        url_field_name = 'topic'
        fields = ('topic', 'name', 'description', 'tags')

"""
class CollectionSerializer(serializers.HyperlinkedModelSerializer):

    resources = serializers.HyperlinkedIdentityField(view_name='resource-detail')
    class Meta:
        model = Collection
        fields = ('name','resources')        
"""

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    
    topics = TopicDetailSerializer(many=True, read_only=True)
    feeds = ResourceContainerSerializer(many=True, read_only=True)
    resources = ResourceDetailSerializer(many=True, read_only=True)    
    class Meta:
        model = Collection
        fields = ('url', 'name', 'description', 'topics', 'resources',)

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

#######################################################################
# Update API
#######################################################################

class CollectionUpdateSerializer(serializers.HyperlinkedModelSerializer):
    
    topics = serializers.PrimaryKeyRelatedField(many=True)
    resources = serializers.PrimaryKeyRelatedField(many=True)
    feeds = serializers.PrimaryKeyRelatedField(many=True)
    class Meta:
        model = Collection
        fields = ('url', 'name', 'description', 'feeds', 'topics', 'resources')


class TopicUpdateSerializer(serializers.HyperlinkedModelSerializer):

    tags = TagListSerializer(required=False)
    collection = serializers.HyperlinkedRelatedField(view_name='collection-detail')
    class Meta:
        model = Topic
        url_field_name = 'topic'
        fields = ('topic', 'collection', 'name', 'description', 'tags')

class InterestUpdateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resource
        url_field_name = 'topic'
        fields = ('interest_hontza', 'interest_social', 'interest_resource')        

#######################################################################
# Upload files
#######################################################################

class AssetSerializer(serializers.ModelSerializer):

    link = serializers.SerializerMethodField('get_absolute_url')
    def get_absolute_url(self, obj):
        return obj.source.url

    class Meta:
        model = File     
        fields = ('id','collection', 'name', 'source')   
