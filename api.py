from tastypie.resources import ModelResource
from mashcast.models import *
from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
import datetime



class CORSResource(Resource):
    """
    Adds CORS headers to resources that subclass this.
    @see: https://gist.github.com/robhudson/3848832
    """
    def create_response(self, *args, **kwargs):
        response = super(CORSResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
 
    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []
 
        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))
 
        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)
 
        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)
 
        return request_method


def _queryize(request, query):
    """
    Narrow the query with the
    query data
    """
    if 'country' in request.GET:
        query = query.filter(countries__in=[Country.objects.get(id=request.GET.get('country'))])
    if 'category' in request.GET:
        query = query.filter(categories__in=[Category.objects.get(id=request.GET.get('category'))])
    if 'language' in request.GET:
        query = query.filter(languages__in=[Language.objects.get(id=request.GET.get('language'))])
    if 'channel' in request.GET:
        query = query.filter(channels__in=[Channel.objects.get(id=request.GET.get('channel'))])
    
    if 'order' in request.GET:
        query = query.order_by(request.GET.get('order'))

    return query

class FeatureResource(CORSResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    text = fields.CharField(attribute='text')
    image = fields.CharField(attribute='image')
    
    class Meta:
        resource_name = 'feature'
        object_class = Channel

    def get_object_list(self, request):
        
        query = Feature.objects.filter(start__lt=datetime.datetime.now(), end__gt=datetime.datetime.now())
        items = []
        for item in list(query):
            # release.spotify_uri = 'spotify:undefined'
            items.append(item)
        return items

    def obj_get(self, bundle, **kwargs):
        item = Feature.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs


class ChannelResource(CORSResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    description = fields.CharField(attribute='description')
    header_image_url = fields.CharField(attribute='header_image_url')
    image = fields.CharField(attribute='image_url')
    podcasts = fields.ToManyField('mashcast.api.PodcastResource', full=True, attribute=lambda bundle: Podcast.objects.filter(channels__in=[bundle.obj]), related_name='podcast')
    class Meta:
        resource_name = 'channel'
        object_class = Channel

    def get_object_list(self, request):
        
        query = Channel.objects.filter()
        query = _queryize(request, query)
       
       
        return list(query)

    def obj_get(self, bundle, **kwargs):
        item = Channel.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs


class CategoryResource(CORSResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    image_url = fields.CharField(attribute='image_url')
    icon = fields.CharField(attribute='icon', null=True, default='bullseye')
    # description = fields.CharField(attribute='description')
    class Meta:
        resource_name = 'category'
        object_class = Category

    def get_object_list(self, request):
        query = Category.objects.filter().order_by('name')
        query = _queryize(request, query)
        items = []
        for item in list(query):
            # release.spotify_uri = 'spotify:undefined'
            items.append(item)
        return items

    def obj_get(self, bundle, **kwargs):
        item = Category.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs

class LanguageResource(CORSResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    class Meta:
        resource_name = 'language'
        object_class = Language

    def get_object_list(self, request):
        query = Country.objects.filter().order_by('name')
        query = _queryize(request, query)
        items = []
        for item in list(query):
            # release.spotify_uri = 'spotify:undefined'
            items.append(item)
        return items

    def obj_get(self, bundle, **kwargs):
        item = Country.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs



class AuthorResource(CORSResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    header_image_url = fields.CharField(attribute='image_url')
    header_image_url = fields.CharField(attribute='header_image_url')
    class Meta:
        resource_name = 'author'
        object_class = Author

    def get_object_list(self, request):
        query = Country.objects.filter().order_by('name')
        query = _queryize(request, query)
        items = []
        for item in list(query):
            # release.spotify_uri = 'spotify:undefined'
            items.append(item)
        return items

    def obj_get(self, bundle, **kwargs):
        item = Country.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs

class CountryResource(CORSResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    class Meta:
        resource_name = 'country'
        object_class = Country

    def get_object_list(self, request):
        query = Country.objects.filter().order_by('name')
        query = _queryize(request, query)
        items = []
        for item in list(query):
            # release.spotify_uri = 'spotify:undefined'
            items.append(item)
        return items

    def obj_get(self, bundle, **kwargs):
        item = Country.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs


class PodcastResource(CORSResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    url = fields.CharField(attribute='url')
    biography = fields.CharField(attribute='description')
    image_url = fields.CharField(attribute='image_url')
    header_image_url = fields.CharField(attribute='header_image_url')
    image = fields.CharField(attribute='image_url', null=True)
    schedule_url = fields.CharField(attribute='schedule_url', null=True)
    author = fields.ToOneField('mashcast.api.AuthorResource', attribute='author')
    class Meta:
        resource_name = 'podcast'
        object_class = Podcast

    def get_object_list(self, request):
        query = Podcast.objects.filter().order_by('-created', 'name')
        query = _queryize(request, query)
        items = []
        for item in list(query):
            if item.schedule_url is None:
                item.schedule_url = ''
            # release.spotify_uri = 'spotify:undefined'
            items.append(item)
        return items

    def obj_get(self, bundle, **kwargs):
        item = Podcast.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs


class EpisodeResource(CORSResource):
    name = fields.CharField(attribute='name')
    description = fields.CharField(attribute='description')
    id = fields.CharField(attribute='id')
    url = fields.CharField(attribute='url')
    pub_date = fields.DateTimeField(attribute='pub_date')
    podcast = fields.ToOneField('mashcast.api.PodcastResource', attribute='podcast')

    class Meta:
        resource_name = 'episode'
        object_class = Episode

    def get_object_list(self, request):
        query = Episode.objects.filter().order_by('-pub_date', 'name')
        query = _queryize(request, query)
        items = []
        for item in list(query):
            items.append(item)
        return items

    def obj_get(self, bundle, **kwargs):
        item = Podcast.objects.get(id=kwargs['pk'])
        return item

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def rollback(self, bundles):
        pass

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs
