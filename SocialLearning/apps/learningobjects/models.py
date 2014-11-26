from django.db import models
from taggit.managers import TaggableManager
from redactor.fields import RedactorField
import random 

# Create your models here.

class SocialNetwork(models.Model):
    name = models.CharField(max_length=255)
    descripcion = RedactorField(null=True, blank=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name

class SocialProfile(models.Model):
    username = models.CharField(max_length=255)
    social_network = models.ForeignKey(SocialNetwork,related_name="profiles",)
    url = models.URLField(max_length=255)
    descripcion = RedactorField(null=True, blank=True)

    def get_interest(self):
        return round(random.uniform(0, 1) * 100) / 100.0

    def get_relevance(self, topic):
        return round(random.uniform(0, 1) * 100) / 100.0
        
    def __unicode__(self):
        return self.username + '@' + str(self.social_network)

class ResourceContainer(models.Model):    
    url = models.URLField()
    rss = models.URLField()
    name = models.CharField(max_length=255, null=True, blank=True)
    descripcion = RedactorField(null=True, blank=True)
    last_processed = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.url 

class Topic(models.Model): 
    name = models.CharField(max_length=255)
    tags = TaggableManager()    

    def __unicode__(self):
        return self.name

class Resource(models.Model):

    ADDED = 0;
    DESCRIBED = 1;
    DISCOVERED = 2;
    EXPANDED = 3;

    RESOURCES_STATUS = (
        (ADDED, 'Added'),
        (DESCRIBED, 'Described'),
        (DISCOVERED, 'Discovered'),
        (EXPANDED, 'Expanded'),
    )

    identifier = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=255)
    url = models.URLField()
    container = models.ForeignKey(ResourceContainer,related_name="resources", null=True, blank=True)
    description = RedactorField(null=True, blank=True)    
    seen_at = models.ManyToManyField(SocialProfile, null=True, blank=True, related_name='resources', through='Mention')
    relevant = models.ManyToManyField(Topic, null=True, blank=True, related_name='resources', through='Relevance')
    last_processed = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0, choices=RESOURCES_STATUS )
    tags = TaggableManager()
    _interest = models.FloatField(default=0.0)
    fulltext = RedactorField(null=True, blank=True) 

    def __unicode__(self):
        return self.title

    @property
    def interest(self):
        return self._interest

    @interest.setter
    def interest(self, value):
        self._interest = value

    def get_relevance(self, topic):

        try:
            rel = Relevance.objects.get(resource=self, topic__name = topic)
            return rel.score
        except:
            return 0.0

    def find_mentions(self):
        return self.title

    def save(self, *args, **kwargs):
        #self.identifier = "" # sha1
        super(Resource, self).save(*args, **kwargs)

    @property
    def topic_list(self):
        return [t.name for t in self.relevant.all()]

class Collection(models.Model):
    name = models.CharField(max_length=255)
    resources = models.ManyToManyField(Resource, null=True, blank=True, related_name="collections")

    def __unicode__(self):
        return self.name

class Mention(models.Model): 
    profile = models.ForeignKey(SocialProfile,related_name="mentions",)
    resource = models.ForeignKey(Resource,related_name="mentions",)
    card = RedactorField(null=True, blank=True)
    tags = TaggableManager()

    def __unicode__(self):
        return u"%s by %s" % (self.resource, self.profile)

class Relevance(models.Model): 
    resource = models.ForeignKey(Resource,related_name="topics",) 
    topic = models.ForeignKey(Topic,related_name="relevance",)     
    score = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-score']

    def __unicode__(self):
        return u"%s scores %f at %s" % (self.resource, self.score, self.topic)

class Scores(models.Model): 
    resource = models.ForeignKey(Resource,related_name="scores",) 
    topic = models.CharField(max_length=255)
    score = models.FloatField(default=0.0)

    def __unicode__(self):
        return u"%s scores %f at %s" % (self.resource, self.score, self.topic)