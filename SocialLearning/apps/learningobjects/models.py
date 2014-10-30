from django.db import models
from redactor.fields import RedactorField

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
    url = models.URLField()
    descripcion = RedactorField(null=True, blank=True)

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

    identifier = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=255)
    url = models.URLField()
    container = models.ForeignKey(ResourceContainer,related_name="resources", null=True, blank=True)
    category = models.CharField(max_length=255)
    description = RedactorField(null=True, blank=True)    
    seen_at = models.ManyToManyField(SocialProfile, null=True, blank=True, related_name='resources', through='Mention')
    last_processed = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0, choices=RESOURCES_STATUS )

    def __unicode__(self):
        return self.title

    def find_mentions(self):
        return self.title

class Collection(models.Model):
    name = models.CharField(max_length=255)
    resources = models.ManyToManyField(Resource, null=True, blank=True, related_name="collections")

    def __unicode__(self):
        return self.name

class Mention(models.Model): 
    profile = models.ForeignKey(SocialProfile,related_name="mentions",)
    resource = models.ForeignKey(Resource,related_name="mention",)
    card = RedactorField(null=True, blank=True)

    def __unicode__(self):
        return "%s by %s" % (self.resource, self.profile)

class Scores(models.Model): 
    resource = models.ForeignKey(Resource,related_name="scores",) 
    topic = models.CharField(max_length=255)
    score = models.FloatField()

    def __unicode__(self):
        return "%s scores %f at %s" % (self.resource, self.score, self.topic)