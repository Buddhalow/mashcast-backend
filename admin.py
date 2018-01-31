from django.contrib import admin
from mashcast.models import *
# Register your models here.
admin.site.register(Podcast)
admin.site.register(Channel)
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Author)