#-*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from django.db import models
from taggit.managers import TaggableManager
from redactor.fields import RedactorField
import random 
import hashlib
from suit_redactor.widgets import RedactorWidget
import feedparser
from datetime import datetime

from learningobjects.utils.search import *
from learningobjects.utils.parsers import *

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
    
    def describe(self):
        d = feedparser.parse(self.rss)
        name = d['feed']['title']

    def latest(self):

        d = feedparser.parse(self.rss)

        res = ()
        for e in d.entries:
            r = Resource(url=e.link, container=self)
            r.save()
            res.append(r)

        self.last_processed = datetime.now()
        self.save()

        return res


    def __unicode__(self):
        return self.url 

class Resource(models.Model):


    ADDED = 0
    DESCRIBED = 1
    DISCOVERED = 2
    EXPANDED = 3
    ERROR = 501
    UNKOWN = 502

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
    local_file = models.FileField(_('file'), upload_to='uploads', null=True, blank=True)
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

    def describe(self):
        try:
            self.status=Resource.DESCRIBED
            url = self.url
            self.identifier = hashlib.md5(url).hexdigest()
            u = URLObject(url)
            print "%s (%s)" % (u.url, u.content_type)
            if 'application/pdf' in u.content_type:
                pd = PDFParser(url).describe()
                self.fulltext = pd.fulltext
                self.content_type = 'PDF'

            # slideshare
            elif bool(re.match('^(http(s|):\/\/|)(www.|)slideshare.net',u.url)):
                s = slides.get_slideshow(slideshow_url=u.url)
                self.title = slide['Slideshow']['Title']
                self.description = slide['Slideshow']['Description']
                self.author = slide['Slideshow']['Username']
                self.fulltext = slide['Slideshow']['Embed']
                self.interest = int(slide['Slideshow']['NumViews']) + int(slide['Slideshow']['NumFavorites']) + int(slide['Slideshow']['NumDownloads'])

                rc_url = 'https://www.slideshare.net/' + slide['Slideshow']['Username'] + '/presentations'
                rc_rss = 'http://es.slideshare.net/rss/user/' + slide['Slideshow']['Username']
                rc, created = ResourceContainer.objects.get_or_create(url=rc_url, rss=rc_rss, name=slide['Slideshow']['Username'] )
            
                rc.resources.add(self)

            # youtube
            elif bool(re.match('^(http(s|):\/\/|)(www.|)youtube.com',u.url)):
                yt_desc = YoutubeParser(url).describe()
                self.title = yt_desc.title
                self.description = yt_desc.description
                self.interest = yt_desc.viewcount
                self.content_type = 'VIDEO'

                self.author = yt_desc.username

                rc_url = 'https://www.youtube.com/user/' + yt_desc.username
                rc_rss = 'http://gdata.youtube.com/feeds/api/users/' + yt_desc.username + '/uploads'
                rc = ResourceContainer.objects.get_or_create(url=rc_url, rss=rc_rss, name=yt_desc.username )
            
                rc.resources.add(self)

            elif 'text/html'  in u.content_type:
                
                rp_desc = ReadibilityParser(url).describe()
                gp_desc = GooseParser(url).describe()
                sm_desc = SummaryParser(url).describe()

                self.title = rp_desc.title
                self.description = sm_desc.summary
                self.fulltext = gp_desc.text
                np = TextBlob(gp_desc.text)
                self.language = np.detect_language()
                self.author = rp_desc.author
                self.content_type = 'WEB'

            else:
                self.status=Resource.UNKOWN

        except:
            self.status=Resource.ERROR

        self.save()

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

    def expand_resources(self):
        for r in self.resources.filter(status='ADDED'):
            r.describe()

    def expand_files(self):
        for f in files:
            r = Resource(url=f.source.url)
            r.local_file.path = f.source.url.replace('/media/','')
            r.save()
            r.describe()
            self.resources.add(r)

    def expand_feeds(self):
        for f in self.feeds: 
            #res = f.describe()
            for r in f.latest:
                self.resources.add(r)

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