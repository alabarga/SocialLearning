#-*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from django.db import models
from taggit.managers import TaggableManager
from redactor.fields import RedactorField
import random 
import hashlib
from suit_redactor.widgets import RedactorWidget

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
    url = models.URLField(null=True, blank=True)
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

    RESOURCES_TYPE = (
        ('WEB', 'Web page'),
        ('BLOG', 'Blog post'),
        ('PDF', 'PDF file'),
        ('VIDEO', 'Video'),
    )

    RESOURCES_LANG = (
        ('es', u'Español'),
        ('en', u'Inglés'),
    )

    identifier = models.CharField(max_length=40, null=True, blank=True, unique=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField()
    domain = models.CharField(max_length=255,null=True, blank=True)
    content = models.CharField(max_length=10, default='WEB', choices=RESOURCES_TYPE )
    language = models.CharField(max_length=255, null=True, blank=True)

    description = RedactorField(null=True, blank=True)    
    fulltext = RedactorField(null=True, blank=True) 
    tags = TaggableManager(blank=True)

    last_processed = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0, choices=RESOURCES_STATUS )

    _interest = models.FloatField(default=0.0)
    interest_hontza = models.FloatField(default=0.0)
    interest_resource = models.FloatField(default=0.0)
    interest_social = models.FloatField(default=0.0)

    container = models.ForeignKey(ResourceContainer,related_name="resources", null=True, blank=True)    
    seen_at = models.ManyToManyField(SocialProfile, null=True, blank=True, related_name='resources', through='Mention')
    relevant = models.ManyToManyField('Topic', null=True, blank=True, related_name='resources', through='Relevance')

    def __unicode__(self):
        if self.title is None:
            return self.url
        else:
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
        if self.pk is None:
            self.identifier = hashlib.md5(self.url).hexdigest() # sha1
        super(Resource, self).save(*args, **kwargs)

    @property
    def topic_list(self):
        return [t.name for t in self.relevant.all()]

class Collection(models.Model):

    CANCELLED = 0
    ADDED = 1;
    DESCRIBED = 2;
    DISCOVERED = 3;
    EXPANDED = 4;

    COL_STATUS = (
        (CANCELLED, 'Cancelled'),        
        (ADDED, 'Added'),
        (DESCRIBED, 'Described'),
        (DISCOVERED, 'Discovered'),
        (EXPANDED, 'Expanded'),
    )

    name = models.CharField(max_length=255)
    description = RedactorField(null=True, blank=True) 
    tags = TaggableManager(blank=True)
    status = models.IntegerField(default=ADDED, choices=COL_STATUS)
    resources = models.ManyToManyField(Resource, null=True, blank=True, related_name="collection")
    feeds = models.ManyToManyField(ResourceContainer, null=True, blank=True, related_name="collection")

    def __unicode__(self):
        return self.name

class File(models.Model):
    collection = models.ForeignKey(Collection,related_name="files",)
    name = models.CharField(max_length=255,null=True, blank=True)
    descripcion = RedactorField(null=True, blank=True)
    source = models.FileField(_('file'), upload_to='uploads',)

    def __unicode__(self):
        return self.name

class Topic(models.Model): 
    collection = models.ForeignKey(Collection,related_name="topics",)
    name = models.CharField(max_length=255)
    description = RedactorField(null=True, blank=True)
    tags = TaggableManager(blank=True)    

    def __unicode__(self):
        return self.name

class Mention(models.Model): 
    profile = models.ForeignKey(SocialProfile, related_name="mentions",)
    resource = models.ForeignKey(Resource, related_name="mentions",)
    card = RedactorField(null=True, blank=True)
    tags = TaggableManager(blank=True)

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