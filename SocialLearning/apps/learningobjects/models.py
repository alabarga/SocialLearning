from django.db import models
from redactor.fields import RedactorField

# Create your models here.

class Collection(models.Model):
    name = models.CharField(max_length=255)
    resources = models.ManyToManyField(Resource, null=True, blank=True, related_name="collections")

    def __unicode__(self):
        return self.name

class SocialProfile(models.Model):
    username = models.CharField(max_length=255)
    social_network = models.ForeignKey(SocialNetwork,related_name="profiles",)
    url = URLField()
    descripcion = RedactorField(null=True, blank=True)

    def __unicode__(self):
        return self.username + '@' + self.social_network
   
class SocialNetwork(models.Model):
    name = models.CharField(max_length=255)
    descripcion = RedactorField(null=True, blank=True)
    url = URLField()

    def __unicode__(self):
        return self.name

class Resource(models.Model):
    pk = models.CharField(max_length=20,null=True, blank=True)
    title = models.CharField(max_length=255)
    url = URLField()
    category = models.CharField(max_length=255)
    description = RedactorField(null=True, blank=True)    
    seen_at = models.ManyToManyField(SocialProfile, null=True, blank=True, related_name="resources")
    last_processed = models.DateTimeField(null=True, blank=True, through='Mention')

    def __unicode__(self):
        return self.title

    def find_mentions(self):
        return self.title

class Mention(models.Model): 
    profile = models.ForeignKey(SocialProfile,related_name="mentions",)
    resource = models.ForeignKey(Resource,related_name="scores",)
    card = RedactorField(null=True, blank=True)

    def __unicode__(self):
        return "%s by %s" % (self.resource, self.profile)

class Scores(models.Model): 
    resource = models.ForeignKey(Resource,related_name="scores",) 
    topic = models.CharField(max_length=255)
    score = FloatField()

    def __unicode__(self):
        return "%s scores %f at %s" % (self.resource, self.score, self.topic)