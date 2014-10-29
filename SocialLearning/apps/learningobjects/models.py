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

class Resource(models.Model):
    primary_key = models.CharField(max_length=20,null=True, blank=True)#si realmente se quiere como pk (primary_key=True), pero null=True y blank=True?
    title = models.CharField(max_length=255)
    url = models.URLField()
    category = models.CharField(max_length=255)
    description = RedactorField(null=True, blank=True)    
    seen_at = models.ManyToManyField(SocialProfile, null=True, blank=True, related_name="resources")
    #last_processed = models.DateTimeField(null=True, blank=True, through='Mention') ///No se que querias hacer aqui, pero el through no se utiliza solo cuando son many to many?

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