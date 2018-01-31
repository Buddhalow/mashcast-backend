from django.shortcuts import render
from django.http import JsonResponse

import feedparser

from mashcast.models import Podcast


def get_feed(request):
  url = request.GET.get('url')

  result = feedparser.parse(url)
  feed = result.feed
  items = result.entries
  podcast = None
  try:
    podcast = Podcast.objects.get(feed_url=url)
  except:
    podcast = Podcast(feed_url=url)
  
  podcast.name = feed.title
  podcast.description = feed.description
  
  try:
    podcast.save()
  except:
    pass
  
  podcast.sync_episodes()

  result = podcast.to_feed_dict()
  return JsonResponse(result)
