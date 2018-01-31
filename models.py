from django.db import models
from django.contrib.auth.models import *
import datetime
import random
import feedparser
from dateutil import parser

def _random_string(length=25):
    characters = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVv0123456789'
    output = ''
    for i in range(length):
        char = characters[random.randint(0, len(characters)-1)]
        output = output + char
    return output

class Author(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    header_image_url = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Author, self).save(args, kwargs)


# Create your models here.
class Category(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField()
    image_url = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Category, self).save(args, kwargs)
        
class Feature(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    url = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Feature, self).save(args, kwargs)
    def __unicode__(self):
        return self.name

class Language(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Language, self).save(args, kwargs)
    def __unicode__(self):
        return self.name

class Country(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Country, self).save(args, kwargs)
    def __unicode__(self):
        return self.name

class Channel(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.datetime.now)
    image_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    countries = models.ManyToManyField(Country)
    categories = models.ManyToManyField(Category)
    verified = models.BooleanField(default=False)
    header_image_url = models.URLField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    languages = models.ManyToManyField(Language)
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Channel, self).save(args, kwargs)

class Podcast(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    url = models.URLField()
    name = models.CharField(max_length=255)
    channels = models.ManyToManyField(Channel)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    header_image_url = models.URLField(blank=True, null=True)
    image_url = models.URLField() 
    feed_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    verified = models.BooleanField(default=False)
    schedule_url = models.URLField(null=True, blank=True)
    countries = models.ManyToManyField(Country)
    languages = models.ManyToManyField(Language)
    created = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
  
    def to_feed_dict(self):
      return dict(
        name=self.name,
        url=self.url,
        feed_url=self.feed_url,
        objects=[
          episode.to_dict() for episode in Episode.objects.filter(podcast=self)
        ]
      )
      
    def sync_episodes(self):
        """ Sync episodes from provider """
        result = feedparser.parse(self.feed_url)
        feed = result.feed
        items = result.entries
        for entry in items:
            published = parser.parse(entry.published)
            
            try:
              episode = Episode.objects.get(podcast=self, pub_date=published)
            except:
              episode = Episode(podcast=self, pub_date=published)
             
            episode.podcast = self
            episode.pub_date=published
            episode.description=entry.summary
            episode.media_url=entry.links[0].href
            episode.name=entry.title
            episode.save()
            
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Podcast, self).save(args, kwargs)


class Episode(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    url = models.URLField()
    name = models.CharField(max_length=255)
    header_image_url = models.URLField(blank=True, null=True)
    image_url = models.URLField() 
    description = models.TextField()
    verified = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True)
    media_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
      
    def to_dict(self):
      return dict(
        name=self.name,
        url=self.url,
        image_url=self.image_url,
        description=self.description,
        verified=self.verified,
        media_url=self.media_url,
        created=self.created,
        pub_date=self.pub_date
      )
      
    def sync(self, entry):
        self.name = entry.title
        self.pub_date = entry.date
        self.description = entry.description

    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Episode, self).save(args, kwargs)
