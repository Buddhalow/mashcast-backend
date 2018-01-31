from django.conf.urls import include, re_path

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from mashcast.api import *

v1_api = Api(api_name='v1')
v1_api.register(PodcastResource())
v1_api.register(FeatureResource())

v1_api.register(CategoryResource())
v1_api.register(ChannelResource())
v1_api.register(LanguageResource())
v1_api.register(CountryResource())

import mashcast.views

urlpatterns = [
    re_path(r'^', include(v1_api.urls)),
    re_path(r'^feed', mashcast.views.get_feed)
]